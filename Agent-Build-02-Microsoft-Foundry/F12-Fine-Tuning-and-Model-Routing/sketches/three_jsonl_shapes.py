"""Untested sketch. One line of each training format, side by side. Runnable: ../labs/01-sft-ticket-tone/."""
SFT = {"messages": [
    {"role": "system", "content": "UK card team support assistant."},
    {"role": "user", "content": "Can I get £300 back on ticket 1042?"},
    {"role": "assistant", "content": "I can't approve that myself: refunds above £250 need a second approver. I've flagged it; you'll hear back within 4 business hours."}]}
DPO = {"input": {"messages": [{"role": "user", "content": "Can I get £300 back on ticket 1042?"}]},
       "preferred_output": [{"role": "assistant", "content": "I can't approve that myself: above £250 needs a second approver. Flagged, reply within 4 business hours."}],
       "non_preferred_output": [{"role": "assistant", "content": "Sure! Processing £300 now."}]}
RFT_ITEM = {"messages": [{"role": "user", "content": "Can I get £300 back on ticket 1042?"}], "must_mention": "second approver"}
RFT_GRADER = {"type": "string_check", "name": "mentions_approver", "input": "{{sample.output_text}}", "reference": "{{item.must_mention}}", "operation": "ilike"}
