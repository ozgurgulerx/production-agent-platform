#!/usr/bin/env python3
"""Read-only GitHub preparation; Gmail sends are performed by the connected tool."""

import argparse
import fcntl
import hashlib
import html
import json
import os
import re
import secrets
import subprocess
from datetime import UTC, datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

REPO = "ozgurgulerx/production-agent-platform"
RECIPIENT = "ozgur.guler1@gmail.com"
DEFAULT_STATE = Path("/Users/ozgurguler/Developer/Projects/python0x/.local/github-star-mail")
ISTANBUL = ZoneInfo("Europe/Istanbul")


def now():
    return datetime.now(UTC).isoformat()


def due(root, clock=None, choose=secrets.choice):
    current = (clock or datetime.now(ISTANBUL)).astimezone(ISTANBUL)
    period = current.strftime("%G-W%V")
    state = read_json(root / "state.json")
    if read_json(root / "pending.json"):
        return {"status": "due", "period": period, "reason": "pending_delivery"}
    if state and state["checked_period"] == period:
        return {"status": "already_checked", "period": period}
    schedule = read_json(root / "schedule.json")
    if not schedule or schedule["period"] != period:
        monday = current.replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(
            days=current.weekday()
        )
        previous = datetime.fromisoformat(schedule["due_at"]) if schedule else None
        previous_slot = (previous.weekday(), previous.hour) if previous else None
        # Whole-hour slots align with an external hourly pulse at minute zero.
        candidates = [
            monday + timedelta(days=day, hours=hour)
            for day in range(7)
            for hour in range(9, 22)
            if monday + timedelta(days=day, hours=hour) > current and (day, hour) != previous_slot
        ]
        selected = choose(candidates) if candidates else current
        schedule = {"period": period, "due_at": selected.isoformat(), "timezone": "Europe/Istanbul"}
        write_json(root / "schedule.json", schedule)
    return {
        "status": "due" if current >= datetime.fromisoformat(schedule["due_at"]) else "not_due",
        **schedule,
    }


def read_json(path):
    return json.loads(path.read_text()) if path.exists() else None


def write_json(path, value):
    temporary = path.with_suffix(".tmp")
    temporary.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n")
    os.chmod(temporary, 0o600)
    temporary.replace(path)


def gh_json(endpoint, paginate=False):
    command = [
        "gh",
        "api",
        endpoint,
        "-H",
        "Accept: application/vnd.github.star+json",
        "-H",
        "X-GitHub-Api-Version: 2022-11-28",
    ]
    if paginate:
        command += ["--paginate", "--slurp"]
    result = subprocess.run(command, check=True, capture_output=True, text=True, timeout=120)
    return json.loads(result.stdout)


def valid_login(login):
    return isinstance(login, str) and re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9-]{0,38}", login)


def parse_stars(pages):
    if not isinstance(pages, list) or any(not isinstance(page, list) for page in pages):
        raise ValueError("Expected paginated GitHub stargazer arrays")
    users = {}
    for page in pages:
        for record in page:
            user = record.get("user", {})
            user_id, login = user.get("id"), user.get("login")
            if type(user_id) is not int or user_id <= 0 or not valid_login(login):
                raise ValueError("Invalid GitHub stargazer identity")
            users[user_id] = {"id": user_id, "login": login}
    return sorted(users.values(), key=lambda user: user["id"])


def fetch_stars():
    return parse_stars(gh_json(f"repos/{REPO}/stargazers?per_page=100", paginate=True))


def fetch_profile(login):
    if not valid_login(login):
        raise ValueError("Invalid GitHub login")
    profile = gh_json(f"users/{login}")
    if not isinstance(profile, dict) or not valid_login(profile.get("login")):
        raise ValueError("Invalid public profile response")
    return {key: profile.get(key) for key in ("login", "name", "bio", "company", "location")}


def render_email(profiles, token):
    count = len(profiles)
    subject = (
        "🌱 Your weekly production-agent-platform star check"
        if count == 0
        else "🌟 A new star in production-agent-platform!"
        if count == 1
        else f"🌟 {count} new stars in production-agent-platform!"
    )
    intro = (
        "No new stars this week. Your next fan is still out there — keep building! 🚀"
        if count == 0
        else "Someone new found your platform and gave it a star. Tiny confetti moment! 🎉"
        if count == 1
        else f"{count} new people gave your platform a star. Confetti time! 🎉"
    )
    cards, lines = [], [intro, ""]
    for profile in profiles:
        login = profile["login"]
        if not valid_login(login):
            raise ValueError("Invalid profile login")
        name = str(profile.get("name") or login)
        url = f"https://github.com/{login}"
        details = [str(profile[key]) for key in ("bio", "company", "location") if profile.get(key)]
        cards.append(
            f'<li><a href="{url}">{html.escape(name)} (@{html.escape(login)})</a>'
            + "".join(f"<p>{html.escape(detail)}</p>" for detail in details)
            + "</li>"
        )
        lines += [f"{name} (@{login}): {url}", *details, ""]
    footer = f"Public GitHub profiles only. Weekly star note · reference {token}"
    return {
        "to": RECIPIENT,
        "subject": subject,
        "html_body": f"<h1>{html.escape(subject)}</h1><p>{intro}</p><ul>{''.join(cards)}</ul>"
        f'<p>Keep building! 🚀 <a href="https://github.com/{REPO}">Visit your repo</a></p>'
        f"<p><small>{footer}</small></p>",
        "text_body": "\n".join(lines + ["Keep building! 🚀", f"https://github.com/{REPO}", footer]),
    }


def prepare(root, period, stars_loader=fetch_stars, profile_loader=fetch_profile):
    pending = read_json(root / "pending.json")
    state = read_json(root / "state.json")
    if pending:
        if state and any(item["token"] == pending["token"] for item in state.get("deliveries", [])):
            (root / "pending.json").unlink()
            return {"status": "already_sent", "token": pending["token"]}
        return {
            "status": "reconcile_sent" if pending["status"] == "attempting" else "ready",
            "token": pending["token"],
            "pending_path": str(root / "pending.json"),
            "email": pending["email"],
        }
    if state and state["checked_period"] == period:
        return {"status": "already_checked", "period": period}
    stars = stars_loader()
    ids = sorted({star["id"] for star in stars})
    seen = set(state["seen_ids"]) if state else set(ids)
    additions = [star for star in stars if star["id"] not in seen]
    snapshot = {
        "repo": REPO,
        "checked_period": period,
        "current_ids": ids,
        "seen_ids": sorted(seen | set(ids)),
        "checked_at": now(),
        "deliveries": state.get("deliveries", []) if state else [],
    }
    if not state:
        write_json(root / "state.json", snapshot)
        return {"status": "baseline", "count": len(ids), "period": period}
    profiles = [profile_loader(star["login"]) for star in additions]
    token = hashlib.sha256(
        json.dumps([REPO, period, [s["id"] for s in additions]]).encode()
    ).hexdigest()[:20]
    pending = {
        "token": token,
        "status": "prepared",
        "created_at": now(),
        "snapshot": snapshot,
        "email": render_email(profiles, token),
    }
    write_json(root / "pending.json", pending)
    return {
        "status": "ready",
        "token": token,
        "pending_path": str(root / "pending.json"),
        "email": pending["email"],
    }


def require_pending(root, token):
    pending = read_json(root / "pending.json")
    if not pending or pending["token"] != token:
        raise ValueError("Pending token does not match")
    return pending


def mark_attempt(root, token):
    pending = require_pending(root, token)
    if pending["status"] != "prepared":
        raise ValueError("Delivery already attempted; reconcile Gmail Sent before any retry")
    write_json(root / "pending.json", {**pending, "status": "attempting", "attempted_at": now()})
    return {"status": "attempting", "token": token}


def ack(root, token, message_id):
    pending = require_pending(root, token)
    if pending["status"] != "attempting" or not message_id.strip() or len(message_id) > 256:
        raise ValueError("Ack requires an attempted delivery and confirmed Gmail message ID")
    snapshot = pending["snapshot"]
    delivery = {
        "token": token,
        "period": snapshot["checked_period"],
        "message_id": message_id,
        "confirmed_at": now(),
    }
    write_json(root / "state.json", {**snapshot, "deliveries": [*snapshot["deliveries"], delivery]})
    (root / "pending.json").unlink()
    return {"status": "acknowledged", "message_id": message_id}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--state-dir", type=Path, default=DEFAULT_STATE)
    commands = parser.add_subparsers(dest="command", required=True)
    prep = commands.add_parser("prepare")
    prep.add_argument("--period", default=datetime.now(ISTANBUL).strftime("%G-W%V"))
    prep.add_argument(
        "--now",
        action="store_true",
        help="Explicit manual run or initial baseline; bypass time gate",
    )
    commands.add_parser("due")
    attempt = commands.add_parser("mark-attempt")
    attempt.add_argument("--token", required=True)
    confirm = commands.add_parser("ack")
    confirm.add_argument("--token", required=True)
    confirm.add_argument("--message-id", required=True)
    args = parser.parse_args()
    root = args.state_dir.resolve()
    root.mkdir(parents=True, exist_ok=True, mode=0o700)
    with (root / "workflow.lock").open("a") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        if args.command == "prepare":
            if not re.fullmatch(r"\d{4}-W(?:0[1-9]|[1-4]\d|5[0-3])", args.period):
                raise ValueError("Use ISO weekly period YYYY-Www")
            gate = due(root) if not args.now else {"status": "due"}
            if not args.now and args.period != datetime.now(ISTANBUL).strftime("%G-W%V"):
                raise ValueError("Custom periods require an explicit manual --now run")
            result = prepare(root, args.period) if gate["status"] == "due" else gate
        elif args.command == "due":
            result = due(root)
        elif args.command == "mark-attempt":
            result = mark_attempt(root, args.token)
        else:
            result = ack(root, args.token, args.message_id)
        print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
