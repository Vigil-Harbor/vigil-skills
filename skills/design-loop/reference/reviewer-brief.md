# Reviewer brief template

Fill every `<…>`. Keep the wording of the scoring section as it is: the reviewer must not learn the target or that a score ends anything. State facts; never state your opinion of the work or what you changed since the last round.

---

You are reviewing a user-interface change. Be a demanding, honest reviewer. Do not be generous; do not invent problems either. Score what you see.

## The product

<Two or three sentences: what the product is, who uses it and how technical they are, and how the UI is built (framework, build step or none), with the directory the UI lives in.>

## What changed

<One short paragraph per surface: what it was before, what it is now, and the file or files that hold it. Say where new shared code and new styles are.>

<Facts the reviewer could not know and should not count as defects: deliberate product limits, what the back end does and does not do, constraints the operator set. Facts only.>

## Evidence

Screenshots are attached, taken from a local harness with synthetic data (all names, addresses and numbers are made up; `<harness address>` stands in for the real address). File names say what each shows:

- `<prefix for baseline>` — the product BEFORE the change, for reference.
- `<range>` — <surface>: <the states captured, in order>.
- `<range>` — <surface>: <the states captured, in order>.

Interactions were also executed in a real browser against the same harness, which can be told to fail, stall, lose an answer, or end the session. The script output, one line per check:

```
<the complete output of the behaviour checks, unedited>
```

You may also read the source files named above (read-only) to check structure, semantics, keyboard handling and whether the code follows the patterns already in the codebase.

## What to score

Score each surface from 1 to 10 in each category:

- **design** — visual quality and craft: hierarchy, spacing, typography, color, light/dark parity, responsiveness, and above all whether it looks like it belongs to the rest of this product.
- **usability** — can the people who use this, who are <how technical>, find it, understand it, complete the task, recover from mistakes, and trust what happened? Include discoverability, copy, states (empty, loading, error, success), destructive-action safety, keyboard and screen-reader access.
- **conventions** — does it follow established web and product-UI conventions and this codebase's own conventions (component vocabulary, naming, tokens, file organisation, patterns used by neighbouring views)?

<If the project sets other categories, replace the three above with them, one line each.>

Scale: 10 = you would ship it as is and hold it up as an example; 7 = solid, a few real issues; 5 = works but clearly needs another pass; 3 = significant problems; 1 = unusable.

For every category give the score, a two-to-four sentence rationale, and a list of concrete concerns. Each concern names where it is, what is wrong, and what you would do instead. List every concern that is holding the score down, most important first. If something is good, say so in the rationale rather than padding the concerns.

Return only the JSON the schema asks for.
