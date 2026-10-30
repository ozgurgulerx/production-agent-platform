# Prompt tool (AI Builder prompt; "skill" in the GitHub harness) (reading map K4)

A prompt tool is a parameterised model call the planner can choose. Build: Tools → Add a tool → Prompt → New prompt. Name `Classify ticket tone`; input `message`; instructions: "Classify the customer's tone as one of calm, frustrated, angry. Return only the label."; model: the default, or a **BYO Foundry model** by endpoint + deployment name (GA; chat-completions only, no GPT-5 family, no Responses endpoints, K4). Test with "I was charged twice, this is the third time" → `angry`.

Credits: AI tools basic 1 / standard 15 / premium 100 per 10 responses (K6). C06 picks up the model choice and the fine-tuned-deployment question.
