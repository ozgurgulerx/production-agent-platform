import importlib.util
import io
import json
import tempfile
import unittest
from datetime import datetime, timedelta
from pathlib import Path
from unittest.mock import patch

SCRIPT = Path(__file__).parents[1] / "scripts" / "star_mail.py"
spec = importlib.util.spec_from_file_location("star_mail", SCRIPT)
mail = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mail)


class StarMailTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def prepare(self, stars, period="2026-W42", profiles=None):
        return mail.prepare(
            self.root,
            period,
            lambda: stars,
            lambda login: (profiles or {}).get(login, {"login": login}),
        )

    def test_initial_baseline_never_mails_history(self):
        result = self.prepare([{"id": 1, "login": "old"}])
        self.assertEqual(result["status"], "baseline")
        self.assertFalse((self.root / "pending.json").exists())
        self.assertEqual(self.prepare([{"id": 1, "login": "old"}])["status"], "already_checked")

    def test_same_count_new_id_detected_and_escaped(self):
        self.prepare([{"id": 1, "login": "old"}])
        result = self.prepare(
            [{"id": 2, "login": "new"}],
            "2026-W43",
            {"new": {"login": "new", "name": "<script>", "bio": "a & b"}},
        )
        self.assertEqual(result["status"], "ready")
        pending = json.loads((self.root / "pending.json").read_text())
        self.assertIn("&lt;script&gt;", pending["email"]["html_body"])
        self.assertIn("a &amp; b", pending["email"]["html_body"])
        self.assertEqual(pending["email"]["to"], "ozgur.guler1@gmail.com")
        self.assertEqual(pending["email"]["subject"], "🌟 A new star in production-agent-platform!")
        state = json.loads((self.root / "state.json").read_text())
        self.assertEqual(state["seen_ids"], [1])

    def test_pending_reused_without_network_and_uncertainty_stops(self):
        self.prepare([])
        first = self.prepare([{"id": 2, "login": "new"}], "2026-W43")

        def fail(*args):
            self.fail("Unexpected network call")

        again = mail.prepare(self.root, "2026-W44", fail, fail)
        self.assertEqual(first["token"], again["token"])
        mail.mark_attempt(self.root, first["token"])
        self.assertEqual(
            mail.prepare(self.root, "2026-W44", fail, fail)["status"], "reconcile_sent"
        )

    def test_ack_only_after_attempt_and_duplicate_period_suppressed(self):
        self.prepare([])
        result = self.prepare([{"id": 2, "login": "new"}], "2026-W43")
        with self.assertRaises(ValueError):
            mail.ack(self.root, result["token"], "message-123")
        mail.mark_attempt(self.root, result["token"])
        mail.ack(self.root, result["token"], "message-123")
        self.assertFalse((self.root / "pending.json").exists())
        self.assertEqual(
            self.prepare([{"id": 3, "login": "later"}], "2026-W43")["status"], "already_checked"
        )
        state = json.loads((self.root / "state.json").read_text())
        self.assertEqual(state["deliveries"][0]["message_id"], "message-123")
        self.assertEqual(state["seen_ids"], [2])

    def test_unstar_and_restar_do_not_repeat_notice(self):
        self.prepare([{"id": 1, "login": "old"}])
        for stars, period in [([], "2026-W43"), ([{"id": 1, "login": "old"}], "2026-W44")]:
            result = self.prepare(stars, period)
            self.assertEqual(result["status"], "ready")
            self.assertIn("No new stars", result["email"]["text_body"])
            mail.mark_attempt(self.root, result["token"])
            mail.ack(self.root, result["token"], "quiet-" + period)

    def test_quiet_week_does_not_advance_before_delivery(self):
        self.prepare([])
        original = (self.root / "state.json").read_text()
        result = self.prepare([], "2026-W43")
        self.assertEqual(result["status"], "ready")
        self.assertEqual(original, (self.root / "state.json").read_text())

    def test_failed_profile_keeps_snapshot(self):
        self.prepare([])
        original = (self.root / "state.json").read_text()

        def failure(login):
            raise RuntimeError("API unavailable")

        with self.assertRaises(RuntimeError):
            mail.prepare(self.root, "2026-W43", lambda: [{"id": 2, "login": "new"}], failure)
        self.assertEqual(original, (self.root / "state.json").read_text())
        self.assertFalse((self.root / "pending.json").exists())

    def test_plural_and_public_fields_only(self):
        rendered = mail.render_email(
            [{"login": "a", "email": "private@example.org"}, {"login": "b"}], "abc"
        )
        self.assertIn("2 new stars", rendered["subject"])
        self.assertNotIn("private@example.org", rendered["html_body"])
        self.assertIn("github.com/a", rendered["html_body"])

    def test_pagination_parsing_and_invalid_records(self):
        rows = mail.parse_stars(
            [[{"user": {"id": 1, "login": "one"}}], [{"user": {"id": 2, "login": "two"}}]]
        )
        self.assertEqual([row["id"] for row in rows], [1, 2])
        with self.assertRaises(ValueError):
            mail.parse_stars([[{"user": {"id": 1, "login": "../bad"}}]])

    def test_weekly_gate_persists_choice_and_changes_next_week(self):
        clock = datetime(2026, 10, 14, 12, 0, tzinfo=mail.ISTANBUL)
        result = mail.due(self.root, clock, lambda options: options[0])
        self.assertEqual(result["status"], "not_due")
        chosen = datetime.fromisoformat(result["due_at"])
        self.assertGreater(chosen, clock)
        self.assertEqual(chosen.minute, 0)

        def unexpected(options):
            self.fail("A weekly choice must not be resampled")

        self.assertEqual(mail.due(self.root, chosen, unexpected)["status"], "due")
        next_week = clock + timedelta(days=7)
        next_result = mail.due(self.root, next_week, lambda options: options[-1])
        self.assertNotEqual(next_result["period"], result["period"])
        next_chosen = datetime.fromisoformat(next_result["due_at"])
        self.assertEqual(next_chosen.hour, 21)

    def test_gate_suppresses_completed_week_without_github(self):
        self.prepare([], "2026-W42")
        clock = datetime(2026, 10, 14, 12, 0, tzinfo=mail.ISTANBUL)
        self.assertEqual(mail.due(self.root, clock)["status"], "already_checked")
        self.assertFalse((self.root / "schedule.json").exists())

    def test_gate_pending_resumes_and_exhausted_week_catches_up(self):
        clock = datetime(2026, 10, 18, 22, 0, tzinfo=mail.ISTANBUL)
        result = mail.due(self.root, clock)
        self.assertEqual(result["status"], "due")
        self.assertEqual(datetime.fromisoformat(result["due_at"]), clock)
        self.prepare([], "2026-W41")
        self.prepare([], "2026-W42")
        self.assertEqual(mail.due(self.root, clock)["reason"], "pending_delivery")

    def test_next_week_never_repeats_previous_weekday_and_minute(self):
        clock = datetime(2026, 10, 12, 8, 0, tzinfo=mail.ISTANBUL)
        first = mail.due(self.root, clock, lambda options: options[0])
        second = mail.due(self.root, clock + timedelta(days=7), lambda options: options[0])
        original = datetime.fromisoformat(first["due_at"])
        updated = datetime.fromisoformat(second["due_at"])
        self.assertNotEqual((original.weekday(), original.hour), (updated.weekday(), updated.hour))

    def run_cli(self, *args):
        output = io.StringIO()
        with (
            patch("sys.argv", ["star_mail", "--state-dir", str(self.root), *args]),
            patch("sys.stdout", output),
        ):
            mail.main()
        return json.loads(output.getvalue())

    def test_cli_baseline_gates_network_then_delivery_lifecycle(self):
        response = type("Response", (), {"stdout": "[[]]"})()
        with patch.object(mail.subprocess, "run", return_value=response) as github:
            self.assertEqual(self.run_cli("prepare", "--now")["status"], "baseline")
            self.assertEqual(self.run_cli("prepare")["status"], "already_checked")
            self.assertEqual(self.run_cli("due")["status"], "already_checked")
            self.assertEqual(github.call_count, 1)
            pending = self.run_cli("prepare", "--now", "--period", "2027-W01")
        token = pending["token"]
        self.assertEqual(self.run_cli("mark-attempt", "--token", token)["status"], "attempting")
        self.assertEqual(
            self.run_cli("ack", "--token", token, "--message-id", "gmail-test")["status"],
            "acknowledged",
        )

    def test_public_profile_adapter_limits_fields_and_rejects_bad_identity(self):
        profile = {"login": "public-user", "name": "Public Name", "email": "omit@example.org"}
        response = type("Response", (), {"stdout": json.dumps(profile)})()
        with patch.object(mail.subprocess, "run", return_value=response) as github:
            result = mail.fetch_profile("public-user")
            self.assertNotIn("email", result)
            self.assertIn("users/public-user", github.call_args.args[0])
        with self.assertRaises(ValueError):
            mail.fetch_profile("../bad")
        response = type("Response", (), {"stdout": "{}"})()
        with (
            patch.object(mail.subprocess, "run", return_value=response),
            self.assertRaises(ValueError),
        ):
            mail.fetch_profile("public-user")


if __name__ == "__main__":
    unittest.main()
