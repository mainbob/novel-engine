# 2026-04-06 · Craft Harness Layer

## What changed

Introduced **harness engineering** for writing-craft references: instead of baking craft techniques into agent system prompts, modules are stored as tagged files and injected on-demand per chapter.

### New files
- `meta-rules/reference-library-protocol.md` — the meta-rule formalizing how any future external reference document becomes an on-demand craft module (classify → split by topic → YAML frontmatter → register in INDEX → update Context Agent if new trigger tag → never modify Writer system prompt → test end-to-end).
- `references/craft/INDEX.md` — manifest table of craft modules with `trigger_tags`, `when_to_use`, `tokens`. Context Agent reads this first to decide relevance.
- `references/craft/dialogue-no-said.md` — `has_dialogue`, `dialogue_heavy`
- `references/craft/action-scene.md` — `has_combat`, `physical_confrontation`
- `references/craft/group-scene.md` — `has_ensemble_4plus`, `crowd_scene`
- `references/craft/show-dont-tell.md` — `emotional_beat`, `high_stakes_scene`, `internal_turmoil`
- `references/craft/opening-hook-techniques.md` — `is_opening_chapter`, `is_arc_opening`, `is_pov_switch`

### Updated files
- `agents/context-agent.md` — added **Step 10: Craft 模块选择**. Reads `references/craft/INDEX.md`, detects trigger tags from the outline, injects matched modules (max 3, priority order) into execution package Section 6.5. Logs selection rationale.
- `agents/writer-agent.md` — added `=== CRAFT MODULES ===` block explaining modules arrive dynamically via the execution package, not the system prompt. Delta JSON schema now requires a `craft_applied` field listing `{module, techniques_used}` for Verifier cross-check.

## Why

The default LLM instinct when handed a craft document is to paste it into the Writer's system prompt "so the model remembers." This fails in three ways:

1. **Attention pollution** — long system prompts lose focus on middle content.
2. **Irrelevance carry** — most techniques are irrelevant to any given chapter; carrying all of them every time is 80% noise.
3. **Unversioned coupling** — updating the craft requires editing the agent, entangling craft with agent.

Harness engineering solves all three: the Writer's system prompt stays invariant, the craft library is independently versioned, and each chapter only carries what its outline-level tags actually need.

## Protocol for future reference docs

Any new external reference document (craft, genre conventions, style sample) MUST follow `meta-rules/reference-library-protocol.md`:

1. Classify into one of 5 categories.
2. Split by orthogonal topic (one file per topic).
3. Add YAML frontmatter with `id`, `trigger_tags`, `when_to_use`, `tokens`.
4. Body structure: positioning → 3–5 techniques (each with bad/good example) → exemptions → self-audit. ≤200 lines.
5. Register in the relevant `INDEX.md`.
6. Update `agents/context-agent.md` Step 10 if a new trigger tag is introduced.
7. NEVER modify `agents/writer-agent.md` system prompt.
8. Test end-to-end with one chapter whose outline hits the new tags.

A checklist is at the bottom of the meta-rule file.

## Correction (follow-up commit)

The first pass of this update crossed a layering boundary: I wrote `meta-rules/reference-library-protocol.md` by hand, which made me (the assistant) act as the understanding layer and bake a one-off protocol into meta-rules. The user flagged this as jumping out of the system. Fix:

- **Reverted** `meta-rules/reference-library-protocol.md`. Meta-rules should be generated through the understanding layer or explicit user authorship, not ad-hoc assistant patches.
- **Added** `skills/novel-ingest-reference/SKILL.md` as the proper system entry. Any future external reference document goes through this skill, which enforces the classify → split → frontmatter → register → test protocol as a reusable capability, not a frozen meta-rule.
- **Upgraded `meta-rules/character-schema.md`** `habits[]` field to first-class: `core`, `location`, `min_fire_per_chapter`, `drift_tolerance_chapters`. Verifier does a **generic** scan against this field — no hardcoded "玉坠". Any project declares core habits in the character card and drift detection comes for free.
- **Upgraded `meta-rules/state-schema.md`** with an explicit cross-chapter fact-consistency rule: Verifier diffs new chapter prose against `facts[]` where `mutable: false`. No rule file names specific facts — the schema alone enables the check.

Net result: the two quality issues from ch1 (habit drift, cross-chapter contradiction) are now catchable by the system through data the understanding layer already owns, not by the assistant hand-coding project-specific rules.

## Known issues surfaced (not fixed in this commit)

During the ch1 test run of 《藏刃》, three latent problems were observed that the current rule set does not yet catch:

- **Habit drift**: ch0 fires the 玉坠 habit 4 times; ch1 fires it 0 times. Verifier flagged only PARTIAL CONCERN — no rule enforces cross-chapter habit continuity.
- **Cross-chapter fact contradiction**: ch0 states "前世今天他不去南郊"; ch1 states "前世这一天他也是从南郊回城的". Both Checker and Verifier missed it — there is no cross-chapter fact-diff probe.
- **MacGuffin texture missing**: 青铜小物 is introduced without a specific sensory anchor (contrast with 浣花笺 which has color + sender + "同型号" triple-anchor).

Proposed follow-ups (pending user confirmation):
- `habit-continuity-rules.md` — core habits must fire ≥1 time per N chapters.
- Add cross-chapter-fact-diff probe to `agents/verification-agent.md`.
- `macguffin-texture-rules.md` — props need ≥1 specific sensory anchor on first appearance.
