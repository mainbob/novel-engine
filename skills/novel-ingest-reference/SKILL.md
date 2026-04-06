---
name: novel-ingest-reference
description: Ingest an external reference document (writing craft, genre conventions, style sample) into the engine as on-demand modules. Use this whenever the user hands you a new reference file — never paste the document into an agent system prompt.
---

# /novel-ingest-reference

> System entry for turning external reference documents into structured, trigger-tagged modules that the Context Agent can borrow on-demand per chapter.
>
> **This skill is the ONLY legitimate path for adding external reference material to the engine.** If you find yourself considering pasting a reference document into an agent system prompt, stop and invoke this skill instead.

---

## Why this skill exists

The default instinct when handed a reference document is to embed it into the Writer's system prompt "so the model remembers." That fails in three ways:

1. **Attention pollution** — long system prompts lose focus on middle content.
2. **Irrelevance carry** — most techniques are irrelevant to any given chapter; carrying all of them every time is mostly noise.
3. **Unversioned coupling** — updating the craft means editing the agent, entangling craft with agent.

The correct pattern is harness engineering: store the reference as tagged modules, let the Context Agent select only matching modules per chapter.

---

## Input

One of:
- A file path the user provides (`/Users/.../some-doc.txt`)
- Pasted text in the conversation
- A URL (fetch with WebFetch first)

## Process

### Step 1: Read the document fully

Do not skim. Do not summarize after partial read. The orthogonal topic detection in Step 2 requires you to have seen the whole document.

### Step 2: Classify into a category

| Category | Destination | Loader |
|---|---|---|
| Writing craft / technique (dialogue, action, show-don't-tell, etc.) | `references/craft/` | Context Agent Step 10 |
| Genre conventions (web-novel rhythm, trope catalog) | `references/genre/` | Context Agent Step 10 |
| World-building (project-specific) | `projects/{book}/settings/` | RAG retrieval |
| Hard rule document (POV discipline, forbidden constructs) | `projects/{book}/generated-rules/` or `default-templates/` | Checker scan-all |
| Style sample (a specific author's prose) | `references/style-samples/` | on-demand inline quote |

**If unclear, ask the user.** Do not invent a new directory.

### Step 3: Split by orthogonal topic

A single reference document usually covers multiple orthogonal topics (dialogue + action + group-scene + openings + show-don't-tell is common). **One topic = one file.** Target 500–1500 tokens per module. If a topic exceeds ~200 lines of markdown, split again.

Propose the split to the user before writing files, so they can correct the granularity.

### Step 4: For each module file, write with YAML frontmatter

```yaml
---
id: {kebab-case-unique-id}
trigger_tags: [tag1, tag2, ...]
when_to_use: {one-line human-readable condition}
tokens: ~{approximate token count}
---
```

`trigger_tags` must be detectable from the **outline**, not from prose. Reuse existing tags where possible — see `references/craft/INDEX.md` for the current tag vocabulary. If introducing a new tag, it goes in Step 6.

### Step 5: Body structure (enforced)

Every module body follows the same shape:

1. **Positioning line** — what problem this module solves (1–2 sentences).
2. **3–5 numbered techniques (招式)**, each with:
   - Principle (原则)
   - Bad example (坏例)
   - Good example (好例)
   - Detection rule (检测规则) — how the Writer self-checks
3. **Exemption section (豁免)** — when NOT to apply.
4. **Execution self-audit (optional)** — post-writing checklist.

Hard limit: ≤200 lines per module. If longer, split.

### Step 6: Register in the INDEX

Append a row to `references/{category}/INDEX.md`:

```markdown
| {module-file.md} | {trigger_tags} | {when_to_use} | ~{tokens} |
```

The INDEX is the selector. Context Agent reads the INDEX first and only opens individual modules after a tag match.

### Step 7: Update Context Agent only if necessary

- **New trigger tag** → add detection guidance to `agents/context-agent.md` Step 10 (how to detect the tag from an outline).
- **New scenario category** → add it to the Step 10 priority ordering.
- **Module replaces an older one** → delete the old file and remove its INDEX row. Do not keep both "just in case."

### Step 8: Do NOT touch the Writer system prompt

`agents/writer-agent.md` has one stable `=== CRAFT MODULES ===` section explaining that modules arrive dynamically via the execution package. Never add module content or module-specific guidance to `writer-agent.md`. The Writer's system prompt must stay invariant across craft library additions.

### Step 9: Test the integration

After adding a module, walk through **one** existing or hypothetical chapter outline whose scene tags hit the new module's `trigger_tags`. Verify on paper:

1. Context Agent's craft-selection logic would pick this module.
2. Section 6.5 of the execution package would contain the module's body.
3. Writer's `writer-delta-{N}.json` `craft_applied` would report the module.
4. Verifier's cross-check of `craft_applied` vs prose would be satisfiable.

If any step is unclear, the integration is under-specified — fix before committing.

---

## Anti-patterns (refuse these)

1. **"Let me paste the whole document into writer-agent.md so the model sees it."** No. Follow the protocol.
2. **"This feels foundational, let me always inject it."** No. Even show-don't-tell has triggers (`emotional_beat`, `high_stakes_scene`, `internal_turmoil`). Low-stakes transition chapters do not need it.
3. **"I'll inject all modules just to be safe."** No. Cap is 3. More = attention pollution.
4. **"Let me make the tags more general so it triggers more often."** No. Over-general tags (`always`, `narrative`) defeat on-demand loading.
5. **"The user gave me a new doc, let me invent a new storage location."** No. Use one of the 5 categories in Step 2. If none fit, ask.
6. **"I'll skip frontmatter, it's just docs."** No. Frontmatter IS the contract — without it, the Context Agent cannot select the module.
7. **"I'll write the meta-rule / schema change myself because I know what's needed."** No. Schema changes go through `/novel-blueprint` or explicit user approval, not ad-hoc through this skill. This skill adds modules, not meta-rules.

---

## Checklist (per module added)

- [ ] Document read fully
- [ ] Classified into one of the 5 categories (user confirmed if ambiguous)
- [ ] Split proposal shown to user before writing files
- [ ] YAML frontmatter with `id`, `trigger_tags`, `when_to_use`, `tokens`
- [ ] Body: positioning + 3–5 techniques (bad/good each) + exemptions + self-audit
- [ ] ≤200 lines
- [ ] Registered in the right INDEX.md
- [ ] New trigger tags taught to `context-agent.md` Step 10 (if any)
- [ ] Writer system prompt NOT modified
- [ ] Walk-through integration test passed

---

## Output

- One or more new files under `references/{category}/`
- Updated `references/{category}/INDEX.md`
- Possibly updated `agents/context-agent.md` (only Step 10, only if new tags)
- A short report to the user listing: files created, tags introduced, any Context Agent updates, any integration concerns.
