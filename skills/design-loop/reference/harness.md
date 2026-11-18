# Building the harness

The harness is what lets you change a UI boldly without touching anything real, and what turns "it looks right" into evidence. It has three parts. Keep all three outside the product code unless the operator asks to keep them; if they do, it is its own commit.

## 1. The mock server

One small process that stands in for every server the UI talks to.

- **Serve the real UI files, unmodified.** If the UI has a mock or demo mode, switch it on from the mock (for example by injecting one line into the HTML as it is served), never by editing the UI.
- **Answer every route the UI calls, from memory.** Find the routes by reading the UI code, and match the real response shapes exactly. When the real routes change, the mock follows them, never the other way round.
- **Made-up data only.** Use reserved example domains for email addresses and obviously fictional names and numbers. Nothing copied from a real system.
- **A reset route and a state route.** Every scenario and every check starts from reset. The state route switches the mock into the situations a real server gets into:

  | State | Why it matters |
  |---|---|
  | a read fails | error and retry states |
  | a write is refused | definite-failure messages |
  | a write is **applied, then answers with an error** | the UI must not say "it failed" |
  | a write **never answers** | timeouts; controls must not stay locked |
  | an answer **starts and never finishes** | a timeout that only covers the headers is not a timeout |
  | the session has ended (401) on a read, and on a write | recovery to sign-in, without losing what was typed |
  | every answer is delayed | in-flight states you can screenshot and assert on |
  | an empty list, a list of one, a long list | empty and crowded layouts |

  The three "no clear answer" states are where reviewers find the most serious usability problems. Build them early.

- **Let the runner start the mock.** A runner that starts its own mock on a free port and stops it afterwards cannot be left without one. A mock left running in the background can be stopped under you mid-round; if that happens the round is void.

## 2. The screenshot runner

- **One scenario per state**, not per screen: default, hover-free, each error, each empty state, each confirmation, in-flight, success, partial success.
- **Light and dark, wide and phone width**, for at least the main states of each surface.
- **File names that say what they show.** The reviewer navigates by them.
- **Still frames.** Zero out animation and transition durations, and hide anything decorative that moves. Wait for the page to settle before the shot.
- **Open the images yourself** before they go to the reviewer. Most first-round problems are visible to you.
- Keep each round's images in their own folder so rounds can be compared.

## 3. The behaviour checks

A script that drives a real browser against the mock and asserts what a picture cannot show. One line of output per check, a count at the end, a non-zero exit when any fails.

What to check:

- **Focus**: where it lands when something opens, where it returns when it closes, where it goes when the focused control disappears or is disabled.
- **Keyboard**: every action reachable without a pointer; Escape and Tab do what the pattern implies; a second Enter on a destructive confirmation does the safe thing.
- **Validation**: the whole input is judged, not a trimmed copy; the first invalid control takes focus; pasted junk is refused, not silently cleaned.
- **What the UI says after each mock state above.** Especially: it never states an outcome it cannot know.
- **State that should survive** (a draft through a close, a tab change) and state that should not (a finished entry).
- **Announcements and names**: status changes reach a live region; buttons that repeat in a list have distinguishable accessible names.

How to write them:

- **Add a check with every behaviour fix.** The checks are the only thing that stops a later round from quietly breaking an earlier one.
- **Wait for the thing, not for time.** Read the page after waiting for the element or text you expect. A check that reads in the same instant as the action will fail at random.
- **A check that fails some of the time is telling you something.** Reproduce it with logging before changing the check. A delayed focus call that steals focus from wherever the person has moved on to looks exactly like a flaky test.
- **Use a fake clock for timeouts** rather than waiting them out.
- **Paste the full check output into the reviewer brief.** A reviewer who can only read the source will otherwise say "not verified in a browser" and score accordingly.

## Things that will bite

- **Delayed focus.** Never move focus from a timer. Move it right after the render that needs it, so it cannot land after the person has gone elsewhere.
- **Hooks and early returns.** In component code, state added during a late round ends up below an early return more often than you would think. The behaviour checks catch it only if a check exercises both sides of the return.
- **Stale answers.** When the same list is read from several places, only the newest read may write the result.
- **Line endings and encodings** on mixed-OS checkouts: patch files by matching normalized text and write back in the file's own convention.
