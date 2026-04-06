# Meta-Rule: Reference Library Protocol

> **How external reference documents become on-demand craft modules.**
> This is a meta-rule. It defines the shape of the process, not any specific document.
> When the user hands you a writing-craft document, a genre-conventions document,
> or any other external reference material, **follow this protocol**. Do not
> improvise. Do not dump the document wholesale into an agent system prompt.

---

## Why this rule exists

The default LLM instinct when given a reference document is to paste its content
into the agent's system prompt "so the model remembers it." This is wrong:

1. **Attention pollution**: long system prompts lose attention on middle content.
2. **Irrelevance carry**: most craft techniques are not relevant to any given chapter;
   carrying all of them every time means 80% noise per invocation.
3. **Unversioned coupling**: embedding craft in the agent prompt means updating
   the craft requires editing the agent — the agent and the craft become entangled.

The correct pattern is **harness engineering / on-demand borrowing**: store the
reference as structured modules, tag each module with trigger conditions, and
have the Context Agent select and inject only the matching modules into each
chapter's execution package.

---

## Protocol

When the user gives you a new external reference document:

### Step 1: Classify the document

Determine which of the following categories the document belongs to:

| Category | Destination | Loader |
|---|---|---|
| **Writing craft / technique** (how to write dialogue, action, etc.) | `references/craft/` | Context Agent Step 10 |
| **Genre conventions** (web-novel rhythm, cultivation trope catalog, etc.) | `references/genre/` | Context Agent Step 10 (new sub-step if needed) |
| **World-building** (specific to a project) | `projects/{book}/settings/` | RAG retrieval by semantic chunk |
| **Rule document** (hard constraints, POV discipline, etc.) | `projects/{book}/generated-rules/` or `default-templates/` | Checker / Verifier scan-all |
| **Style model** (a specific author's prose as reference) | `references/style-samples/` | on-demand inline quote |

**Default: if unclear, it's probably `references/craft/`.**

### Step 2: Split by topic

A single reference document often covers multiple orthogonal topics (e.g. the
writer-layer document covered: avoiding 说/道, action scenes, group scenes,
openings, show-don't-tell — 5 orthogonal topics). **Do not store them as one
file.** Split into one file per topic.

Each topic becomes one module file. Module size target: ~500–1500 tokens.
If a topic exceeds 200 lines of markdown, split it further.

### Step 3: Add YAML frontmatter

Every module file must start with frontmatter:

```yaml
---
id: {kebab-case-unique-id}
trigger_tags: [{tag1}, {tag2}, ...]
when_to_use: {one-line human-readable condition}
tokens: ~{approximate token count}
---
```

**`trigger_tags` are the contract** — they are how the Context Agent decides
whether to inject this module. Use tags that are detectable from the outline,
not from the prose. Examples of valid tags:

- `has_dialogue`, `dialogue_heavy`
- `has_combat`, `physical_confrontation`
- `has_ensemble_4plus`, `crowd_scene`
- `emotional_beat`, `high_stakes_scene`, `internal_turmoil`
- `is_opening_chapter`, `is_arc_opening`, `is_pov_switch`
- `has_flashback`, `is_revelation_chapter`, `is_reinforcement_chapter`

If you need a new trigger tag category that doesn't exist yet, you **must**
update `agents/context-agent.md` Step 10 to teach the Context Agent how to
detect it from the outline.

### Step 4: Body structure

Every module body follows the same shape (enforced by INDEX.md rule 模块内部规范):

1. **Positioning line** (what problem this module solves, 1-2 sentences)
2. **3–5 numbered techniques (招式)**, each with:
   - Principle (原则)
   - Bad example (坏例)
   - Good example (好例)
   - Detection rule (检测规则) — how the Writer can self-check
3. **Exemption section** (豁免) — when NOT to apply these techniques
4. **Execution self-audit** (optional) — checklist the Writer runs after writing

**Rule**: if the body exceeds 200 lines, split the module.

### Step 5: Register in INDEX.md

Add a row to `references/{category}/INDEX.md` manifest table:

```markdown
| {module-file.md} | {trigger_tags} | {when_to_use} | ~{tokens} |
```

The INDEX is what the Context Agent reads first — it should never need to
open individual modules to decide relevance. The INDEX is the **selector**.

### Step 6: Update Context Agent if needed

- If the new module introduces a **new trigger tag** → update `agents/context-agent.md`
  Step 10's scenario-detection list with how to detect it from the outline.
- If the new module introduces a **new scenario category** (e.g. "philosophical
  digression") → add it to the priority ordering in Step 10.5 (the tie-breaker
  list used when more than 3 modules match).
- If the new module **replaces** an older one → delete the old file and remove
  from INDEX. Do not keep both "just in case."

### Step 7: Do NOT touch the agent system prompt

The Writer's `agents/writer-agent.md` already has one stable section
(`=== CRAFT MODULES ===`) explaining that modules arrive dynamically via the
execution package. **Never** add the new module's content to writer-agent.md.
Never add module-specific guidance to writer-agent.md. The Writer's system
prompt must stay invariant across craft library additions — only the
execution package varies per chapter.

### Step 8: Test the integration

After adding a module, write one test chapter that has the relevant trigger
tags in its outline. Verify in the resulting `state/context-{N}.md` that:

1. The Context Agent's craft selection log mentions the new module
2. Section 6.5 of the execution package contains the module's full content
3. The Writer's `writer-delta-{N}.json` reports the module in `craft_applied`
4. The Verifier cross-checks `craft_applied` against what's actually in the prose

If any of these fails, the integration is broken — fix it before moving on.

---

## Anti-patterns (critical)

These are the failure modes you must not reach for:

1. **"Let me just paste the whole document into writer-agent.md so the model sees it"**
   → No. Use the protocol above. Every time.

2. **"This reference feels important, let me always inject it"**
   → No. Even foundational techniques like show-don't-tell have triggers
   (`emotional_beat`, `high_stakes_scene`, `internal_turmoil`). A low-stakes
   transition chapter does not need show-don't-tell injected.

3. **"I'll trigger all modules just to be safe"**
   → No. The cap is 3 modules. More = attention pollution. If you feel the
   need to inject more, the chapter outline is doing too much — split the chapter.

4. **"Let me make the module more general so it triggers more often"**
   → No. Modules should be specific. Overly general trigger tags (like
   `always`, `narrative_content`) defeat the whole point of on-demand loading.

5. **"The user gave me a new doc, let me invent a new storage location"**
   → No. Classify it into the 5 categories in Step 1. If none fit, ask the
   user — don't improvise a new directory.

6. **"I'll skip the frontmatter, it's just documentation"**
   → No. The frontmatter IS the contract. Without it, the Context Agent
   cannot select the module, and it's invisible to the pipeline.

---

## Checklist for adding a new reference

- [ ] Classified into one of the 5 categories
- [ ] Split by orthogonal topic (one topic per file)
- [ ] YAML frontmatter with `id`, `trigger_tags`, `when_to_use`, `tokens`
- [ ] Body follows: positioning + 3-5 techniques + exemptions + self-audit
- [ ] Each technique has bad/good example pair
- [ ] Module ≤ 200 lines
- [ ] Registered in INDEX.md manifest table
- [ ] New trigger tags added to `context-agent.md` Step 10 if any
- [ ] Priority ordering updated if new category
- [ ] `writer-agent.md` system prompt NOT modified
- [ ] Test chapter written and pipeline verified end-to-end
