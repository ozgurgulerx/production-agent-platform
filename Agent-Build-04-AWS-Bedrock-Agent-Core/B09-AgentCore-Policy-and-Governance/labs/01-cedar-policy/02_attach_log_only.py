"""Proves: the engine attaches to a gateway through UpdateGateway.policyEngineConfiguration {arn, mode}; LOG_ONLY
means no call is refused yet. UpdateGateway re-sends name, roleArn and authorizer, so we copy them from GetGateway.
Usage: python 02_attach_log_only.py [--mode LOG_ONLY|ENFORCE] [--cleanup]"""
import os
import sys

from _common import GATEWAY_ID, control, need

need("TICKET_GATEWAY_ID", "POLICY_ENGINE_ARN")


def set_mode(mode: str | None) -> dict:
    c = control()
    gw = c.get_gateway(gatewayIdentifier=GATEWAY_ID)
    kwargs = {k: gw[k] for k in ("name", "roleArn", "authorizerType") if k in gw}
    for k in ("description", "protocolType", "protocolConfiguration", "authorizerConfiguration",
              "kmsKeyArn", "interceptorConfigurations"):
        if gw.get(k):
            kwargs[k] = gw[k]
    if mode:
        kwargs["policyEngineConfiguration"] = {"arn": os.environ["POLICY_ENGINE_ARN"], "mode": mode}
        kwargs["exceptionLevel"] = "DEBUG"      # denial bodies carry the policy reason
    # cleanup: omit policyEngineConfiguration -> detached  # verify that omission detaches rather than keeps
    return c.update_gateway(gatewayIdentifier=GATEWAY_ID, **kwargs)


def main() -> None:
    if "--cleanup" in sys.argv:
        r = set_mode(None)
        print("detached; policyEngineConfiguration now:", r.get("policyEngineConfiguration"))
        return
    mode = sys.argv[sys.argv.index("--mode") + 1] if "--mode" in sys.argv else "LOG_ONLY"
    r = set_mode(mode)
    print("gateway", r["gatewayId"], r["status"], "policy:", r.get("policyEngineConfiguration"))


if __name__ == "__main__":
    main()
