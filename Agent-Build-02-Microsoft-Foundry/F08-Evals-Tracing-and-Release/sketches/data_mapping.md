# Data-mapping cheat sheet (untested, from Learn G1/G3)

| placeholder | meaning | use with |
|---|---|---|
| `{{item.query}}`, `{{item.ground_truth}}` | dataset columns | any evaluator |
| `{{sample.output_text}}` | the target agent's text | text quality, safety |
| `{{sample.output_items}}` | full output items incl. tool calls | task adherence, tool call accuracy, tool selection |
| `{{item.response}}`, `{{item.tool_definitions}}` | what live-response and trace sources expose | continuous and scheduled evals |
| `initialization_parameters.deployment_name` | judge model | model-based evaluators |
