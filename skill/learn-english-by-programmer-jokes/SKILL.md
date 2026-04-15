---
name: learn-english-by-programmer-jokes
description: After completing a task, append one short bilingual programmer joke or quote from this repository, preferably matched to the task context.
version: 0.1.0
license: MIT
metadata:
  hermes:
    tags: [humor, bilingual, programmer-jokes, english-learning, final-response]
---

# Learn English By Programmer Jokes

Use this skill when the main task is already complete and you want to end with one short bilingual programmer joke or quote.

## Goal

Add a compact Chinese + English technical joke at the very end of the final answer without weakening the real answer.

## Trigger

Only trigger when:
- the user's primary request has been completed, answered, or clearly wrapped up
- the conversation is not in a sensitive, medical, legal, crisis, grief, or safety-critical context

Do not trigger when:
- the task failed and the user still needs urgent troubleshooting
- the conversation is emotionally heavy or high-stakes
- a joke would make the answer less trustworthy or less professional

## Behavior Rules

- Add at most one joke.
- Keep it short.
- Prefer a joke relevant to the task context.
- Use the topic mapping in `references/joke-selection-rules.md`.
- For quick quote lookup, prefer `references/jokes-by-topic.md` instead of reading the full CSV.
- If no strong topic match exists, fall back to a classic quote.
- Never let the joke replace the real answer.

## Output Format

Use `templates/final-joke-template.txt` as the output shape.

Default format:

技术段子 / Tech Joke
EN: ...
ZH: ...
— Author

## Suggested Workflow

1. Finish the user's actual task.
2. Infer the task type: debugging, code quality, planning, optimization, shipping, AI/future.
3. Pick one matching joke from the references.
4. Append it as a final small section.

## Good Examples

### Debugging task
技术段子 / Tech Joke
EN: Debugging is twice as hard as writing the code in the first place.
ZH: 调试代码比写代码更困难。
— Brian Kernighan

### Code review task
技术段子 / Tech Joke
EN: Code is like humor. When you have to explain it, it's bad.
ZH: 代码就像幽默。当你不得不解释它时，它就是糟糕的。
— Cory House

### Planning task
技术段子 / Tech Joke
EN: First, solve the problem. Then, write the code.
ZH: 首先，解决问题。然后，编写代码。
— John Johnson
