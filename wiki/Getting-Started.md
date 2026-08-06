# 🚀 Getting Started

This page explains how the moving parts of the learning log fit together and how to add to it. The system has three layers that build on each other:

1. **Logs** — a running journal of what you did and learned.
2. **Concepts** — distilled notes on a single idea.
3. **Tags** — the connective tissue that links them together.

## 🧭 The workflow

1. **Log as you go.** After a study or coding session, add a dated entry in [`LOGS/`](../LOGS) using [`logs-template.md`](../LOGS/logs-template.md). Name the file `YYYY-MM-DD-topic.md` — the date in the filename is what the tag indexer uses to order mentions.
2. **Distill into concepts.** When an idea deserves a standalone explanation, create a page in [`concepts/`](../concepts) from [`concepts-template.md`](../concepts/concepts-template.md).
3. **Tag everything.** Sprinkle tags into both logs and concepts so they become searchable (see below).
4. **Regenerate the index.** Run the tag indexer to refresh the cross-references:
   ```bash
   python scripts/generate_tag_index.py
   ```
5. **Define new terms.** Add anything unfamiliar to the [Glossary](Glossary.md).

## 🏷️ Tag conventions

The [tag indexer](../scripts/generate_tag_index.py) understands three formats:

| Format | Example | Meaning |
|---|---|---|
| `#tag` | `#python`, `#Web_Security` | A regular topic tag |
| `#.method()` | `#.append()` | A method |
| `#func()` | `#print()` | A built-in function |

See [`tags/README.md`](../tags/README.md) for the full details, then browse the generated index in the [`tags/`](../tags) folder.

## ✅ Quick checklist for a new entry

- [ ] Created a dated file in `LOGS/` (or a page in `concepts/`)
- [ ] Added relevant `#tags`
- [ ] Added any new terms to the [Glossary](Glossary.md)
- [ ] Ran `python scripts/generate_tag_index.py`

---

_Back to the [Wiki Home](Home.md)._
