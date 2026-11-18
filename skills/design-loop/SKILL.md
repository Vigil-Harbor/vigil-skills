---
name: design-loop
description: Redesign a user interface through a designer/reviewer loop. You design in an isolated working copy on synthetic data and prove each change with screenshots and scripted browser checks; an outside reviewer scores design, usability and conventions without knowing the target; the loop exits when every score reaches it. Use when the operator asks to iterate a UI until it holds up to an independent review, says "design loop" or "review loop the UI", or names surfaces that need a better UI.
user_invocable: true
requires:
  shell: true
  filesystem: [read, write]
  network: true
  subagents: optional
  services: [vcs-host?]
---

# /design-loop — design, prove, get scored, repeat

Invoked as: `/design-loop <the surfaces to redesign>`.

Three roles. **You are the designer**: you make the changes and you prove them. **The reviewer** is a different model in a fresh context, with no stake in the work: it reads the screenshots, the check results and the source, and returns scores with concerns. **The operator** decides what is theirs to decide and reads your report each round.

The loop exits when the reviewer gives every category the target score, on the build that will ship.

## What this skill must not do

- Touch a live system or use production data. All work is in an isolated working copy, against a mock, with made-up data.
- Tell the reviewer the target score, that a score ends the loop, or what you changed since its last round.
- Score your own work. If no outside reviewer can run, stop and say so.
- Count a round whose evidence was incomplete (a check run that crashed, a mock that died, missing screenshots). That round is void; rerun it.
- Claim the exit for code the reviewer has not seen. Changes made after a scoring round are unscored until a confirmation round, and the report says so.
- Merge, deploy, or publish. The end product is a branch or pull request the operator can review.

## Settings

Read the project's instructions (the text the host already supplied, else `CLAUDE.md` then `AGENTS.md` at the project root) for an optional `## Design loop` section. Each line is `key: value`. Anything missing uses the default.

| Key | Default | Meaning |
|---|---|---|
| `target` | `8` | Score every category must reach, out of 10. |
| `categories` | `design, usability, conventions` | What the reviewer scores. |
| `reviewer` | *(ask the operator)* | How to run the outside reviewer: a model name, or a one-line command. |
| `deliverable` | `pull request` | What to produce at the exit. |

If the operator names a reviewer or a target in the request, that wins over the section.

## Step 1 — Ask before starting

Read the surfaces as they are today first, so the questions are informed. Then ask the operator, in one round, only what is theirs to decide. Typical questions:

- **Where each thing should live**, when the request is about finding a home for something. Offer two to four concrete options and recommend one.
- **Scope**: only the named surfaces, or keep going across the product.
- **Boundary**: which parts of the system may change (for example, whether a new read-only route is allowed) and which must not.
- **Deliverable**: pull request, branch only, or something else.

Do not ask about things with an obvious default. State the defaults you are using.

## Step 2 — Set up

1. **An isolated working copy** cut from the default branch (a git worktree, or the equivalent in your host). The primary working tree is never touched.
2. **A harness**, outside the product code unless the operator asks to keep it. Read [`reference/harness.md`](reference/harness.md) before building one. It has three parts:
   - a **mock server** that serves the real UI files unmodified and answers every route the UI calls from memory, with made-up data, and that can be switched into failure states;
   - a **screenshot runner** that captures one image per state;
   - **behaviour checks**, a script that drives a real browser and asserts what a screenshot cannot show.
3. **Baseline screenshots** of the surfaces before any change. They are reference for you and evidence for the reviewer.

## Step 3 — The loop

Each round, in this order:

1. **Design.** Make the change. Be bold in the first round: move things, restructure, give the surface a real home. Later rounds fix what the review found. Match the product's existing visual and code vocabulary; a redesign that looks like a different product fails "belongs here".
2. **Look at it yourself.** Take the screenshots and open them. Fix what you can see is wrong before spending a review on it.
3. **Run the behaviour checks.** Every check passes, or you know exactly why one does not. A check that fails some of the time is a finding, not noise: reproduce it and find the cause before deciding it is the test.
4. **Send the round to the reviewer** (the reviewer contract below).
5. **Gate the scores** with the script:

   ```bash
   SCRIPT="${CLAUDE_CONFIG_DIR:-$HOME/.claude}/skills/design-loop/scripts/score_gate.py"
   command -v python3 >/dev/null 2>&1 && python3 -c '' >/dev/null 2>&1 && PY=python3 || PY=python
   "$PY" "$SCRIPT" <review.json> --target <target> --categories <categories, comma-separated> --concerns
   ```

   Exit code 0 means every category reached the target. 1 means at least one did not. 2 means the review is malformed or incomplete (an empty file from a reviewer that was stopped, a surface missing a category): the round is void.
6. **Work the findings** (next section), then report to the operator (Step 4) and start the next round.

There is no fixed round cap. Keep going while the findings are valid. Stop and ask the operator when a category has not moved for three rounds on repeating findings, when the reviewer's findings have stopped being valid, or when the reviewer hits a usage limit.

### Working the findings

Take each concern on its merits, most severe first.

- **Valid**: fix it, and add a behaviour check for it when it is about behaviour. A fix without a check tends to come back.
- **Not valid**: do not fix it. Note why in your round report.
- **Needs something only the operator has** (a destination, a policy, a product decision): collect it for the operator. Do not invent the answer.
- **Out of scope or not worth its cost**: leave it and say so in the final report.

When findings keep landing in the same mechanism round after round, the mechanism is the problem. Replace it with a simpler model instead of patching it again.

Never trade honesty for a score. If the interface cannot know something (whether a save went through, whether a session is still alive), it says so; it does not guess in either direction.

## The reviewer contract

Run the reviewer in a fresh context every round, with read-only access to the working copy *(e.g. a second-vendor CLI in read-only sandbox mode with the images attached, or a sub-agent on another model; use whatever the operator named)*. A different model family from the designer is the point: it does not share your blind spots.

Build the brief from [`reference/reviewer-brief.md`](reference/reviewer-brief.md) and require the answer in the shape of [`reference/score-schema.json`](reference/score-schema.json). The brief carries:

- what the product is and who uses it;
- what changed, and where the code is;
- the evidence: baseline and current screenshots (file names that say what each shows), and the full output of the behaviour checks;
- the scoring scale and the categories;
- **facts about constraints** the reviewer could not know (a deliberate product limit, what a back end does or does not do). Facts only.

The brief never carries the target score, your opinion of the work, or a list of what you fixed. A reviewer handed your conclusion returns it confirmed.

The reviewer reads the source as well as the pictures. Expect most low usability scores to come from interaction defects it finds in the code (focus, keyboard, what the interface claims after a failed request), not from how the screens look.

## Step 4 — Report each round

After every round, tell the operator, briefly:

- the score table for the round;
- what you changed in response, in plain terms;
- what you did not take, and why;
- anything that went wrong (a void round, a check that turned out to be a real bug).

## Step 5 — Exit

When the gate passes:

1. If anything changed after the scoring round, run one **confirmation round** on the final build, or state plainly which changes are unscored.
2. Run the product's own tests for anything you touched outside the UI.
3. Commit and produce the deliverable. Offer the harness as a separate commit; it is not part of the product change.
4. Give the final report: the scores, what the operator gets, where it differs from what they might expect, what was verified and what was not, and a list of what is waiting on them.

## Failure modes

- **No outside reviewer available**: say `no outside reviewer is available in this host` and stop before Step 3. Design work without the review is a different task; ask whether the operator wants that instead.
- **Reviewer usage limit or error mid-loop**: stop, report the last complete round, and ask.
- **The mock or the browser died during a round**: the round is void. Restart it, rerun the checks to completion, then rerun the review.
- **A tool call is denied**: stop and report it. Do not retry it reworded.
