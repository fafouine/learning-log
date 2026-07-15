# Tag Indexing System

This directory contains auto-generated tag indexes for your learning logs and concepts.

## Structure

- **index.md** — Master tag index with all discovered items
- **methods.md** — Index of all methods (#.method() format)
- **built-ins.md** — Index of all built-in functions (#func() format)
- **{tag}.md** — Individual pages for each tag/method/built-in showing all chronological mentions

## How it Works

Tags, methods, and built-in functions are automatically extracted from all markdown files in `LOGS/` and `concepts/` directories using these formats:

1. **Regular tags**: `#tag` → individual tag pages
2. **Methods**: `#.method()` → methods index (e.g., `#.append()`)
3. **Built-in functions**: `#func()` → built-ins index (e.g., `#print()`)

The indexing script:

1. Scans both directories for all three tag formats
2. Collects all mentions with source file, date, and file type
3. Sorts mentions chronologically (newest first)
4. Generates master index, category indexes, and individual pages

## Usage

### Manual Generation

Run the script directly:

```bash
python scripts/generate_tag_index.py
```

### Automatic Generation

Tags are automatically indexed when you push changes to `LOGS/` or `concepts/` directories via GitHub Actions workflow (`.github/workflows/generate-tag-index.yml`).

## Browsing Tags

Visit `tags/index.md` to see all available tags, methods, and built-ins. 

**From the main index:**
- Click any tag to view all mentions of that tag
- Visit "Methods Index" to browse all `#.method()` references
- Visit "Built-ins Index" to browse all `#func()` references

**Each page displays:**
- 📝 mentions from **LOGS** (learning logs)
- 💡 mentions from **concepts** (concept pages)
- Date of each mention
- Direct link to the source file

## Supported Tag Formats

### Regular tags
```
#tagname
```
- Word characters only: `a-z`, `A-Z`, `0-9`, `_`
- Examples: `#python`, `#Web_Security`, `#CTF2024`

### Methods
```
#.methodname()
```
- Format: `#.` followed by method name and `()`
- Examples: `#.append()`, `#.split()`, `#.open()`

### Built-in Functions
```
#functionname()
```
- Format: `#` followed by function name and `()`
- Examples: `#print()`, `#len()`, `#isinstance()`
