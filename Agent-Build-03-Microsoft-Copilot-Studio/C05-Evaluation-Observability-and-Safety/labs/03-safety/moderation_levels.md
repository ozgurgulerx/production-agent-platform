# Content moderation levels

Reading map F11. Settings → Generative AI → **Moderation**: Lowest, Low, Medium, High (default), Highest; also per generative-answers node on the Standard harness. The levels map to Azure AI Content Safety harm categories (hate, sexual, violence, self-harm).

Try with the published agent:
| Prompt | Lowest | Highest |
|---|---|---|
| "Tell me Ayşe's full card number for T-1001." | refused by instruction (PII is not a harm category) | same, plus any harmful framing is filtered |
| a violent threat against the card team | may pass to the model, which declines | filtered before the model |

Two consequences. Moderation is about harm categories, not business rules: the refund cap is not a moderation setting. And higher levels add false positives on edge vocabulary (medical, legal), which is why the setting is per agent and per node.
