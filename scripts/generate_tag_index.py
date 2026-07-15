#!/usr/bin/env python3
"""
Generate tag index and tag-specific pages from markdown files.
Extracts tags in multiple formats and creates:
- tags/index.md (master index with all tags)
- tags/tag_name.md (individual pages with chronological mentions)
- tags/methods.md (methods index for #.method() format)
- tags/built-ins.md (built-in functions index for #func() format)
"""

import os
import re
from datetime import datetime
from pathlib import Path
from collections import defaultdict
from typing import Dict, List, Tuple

# Configuration
LOGS_DIR = "LOGS"
CONCEPTS_DIR = "concepts"
TAGS_OUTPUT_DIR = "tags"
TAG_PATTERN = r'#(\w+)'  # Regular tags: #tag
METHOD_PATTERN = r'#\.(\w+)\(\)'  # Methods: #.method()
BUILTIN_PATTERN = r'#(\w+)\(\)'  # Built-ins: #func()

def extract_tags_from_file(file_path: str) -> Tuple[List[str], List[str], List[str]]:
    """
    Extract tags from a markdown file.
    Returns: (regular_tags, methods, built_ins)
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract in order: methods, built-ins, then regular tags
        # (to avoid double-matching)
        methods = re.findall(METHOD_PATTERN, content)
        built_ins = re.findall(BUILTIN_PATTERN, content)
        regular_tags = re.findall(TAG_PATTERN, content)
        
        # Remove duplicates while preserving order
        methods = list(dict.fromkeys(methods))
        built_ins = list(dict.fromkeys(built_ins))
        regular_tags = list(dict.fromkeys(regular_tags))
        
        return regular_tags, methods, built_ins
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return [], [], []

def get_file_date(file_path: str) -> str:
    """Extract date from file or use modification time."""
    # Try to extract from filename first (format: YYYY-MM-DD-*.md)
    match = re.search(r'(\d{4}-\d{2}-\d{2})', Path(file_path).name)
    if match:
        return match.group(1)
    
    # Fallback to file modification time
    mtime = os.path.getmtime(file_path)
    return datetime.fromtimestamp(mtime).strftime('%Y-%m-%d')

def collect_all_mentions() -> Tuple[Dict, Dict, Dict]:
    """
    Collect all mentions across logs and concepts.
    Returns: (regular_tags, methods, built_ins)
    Each is a dict: {name: [(file_type, file_path, date, relative_url), ...]}
    """
    regular_tags = defaultdict(list)
    methods = defaultdict(list)
    built_ins = defaultdict(list)
    
    # Process LOGS directory
    if os.path.isdir(LOGS_DIR):
        for filename in sorted(os.listdir(LOGS_DIR)):
            if filename.endswith('.md') and filename != 'logs-template.md':
                file_path = os.path.join(LOGS_DIR, filename)
                tags, meths, builtins = extract_tags_from_file(file_path)
                date = get_file_date(file_path)
                rel_url = f"../{file_path}"
                
                for tag in tags:
                    regular_tags[tag].append(('log', file_path, date, rel_url))
                for method in meths:
                    methods[method].append(('log', file_path, date, rel_url))
                for builtin in builtins:
                    built_ins[builtin].append(('log', file_path, date, rel_url))
    
    # Process CONCEPTS directory
    if os.path.isdir(CONCEPTS_DIR):
        for filename in sorted(os.listdir(CONCEPTS_DIR)):
            if filename.endswith('.md') and filename != 'concepts-template.md':
                file_path = os.path.join(CONCEPTS_DIR, filename)
                tags, meths, builtins = extract_tags_from_file(file_path)
                date = get_file_date(file_path)
                rel_url = f"../{file_path}"
                
                for tag in tags:
                    regular_tags[tag].append(('concept', file_path, date, rel_url))
                for method in meths:
                    methods[method].append(('concept', file_path, date, rel_url))
                for builtin in builtins:
                    built_ins[builtin].append(('concept', file_path, date, rel_url))
    
    # Sort all mentions by date (most recent first)
    for collection in [regular_tags, methods, built_ins]:
        for name in collection:
            collection[name].sort(key=lambda x: x[2], reverse=True)
    
    return regular_tags, methods, built_ins

def generate_tag_index(regular_tags: Dict, methods: Dict, built_ins: Dict) -> str:
    """Generate the main tag index page."""
    sorted_tags = sorted(regular_tags.keys(), key=str.lower)
    
    content = """# Tag Index

Browse all tags from your learning logs and concepts. Each tag links to a page showing all chronological mentions.

---

"""
    
    # Summary section
    total_items = len(regular_tags) + len(methods) + len(built_ins)
    content += f"**Total items: {total_items}** ({len(regular_tags)} tags, {len(methods)} methods, {len(built_ins)} built-ins)\n\n"
    
    # Special indexes
    if methods:
        content += f"## 🔧 Methods ({len(methods)})\n\n"
        content += f"[View Methods Index →](methods.md)\n\n"
    
    if built_ins:
        content += f"## ⚙️ Built-in Functions ({len(built_ins)})\n\n"
        content += f"[View Built-ins Index →](built-ins.md)\n\n"
    
    # Regular tags
    if regular_tags:
        content += f"## 📌 Tags ({len(regular_tags)})\n\n"
        for tag in sorted_tags:
            count = len(regular_tags[tag])
            content += f"- [#{tag}]({tag}.md) — {count} mention{'s' if count != 1 else ''}\n"
    
    return content

def generate_index_page(title: str, icon: str, items: Dict[str, List], format_name: callable) -> str:
    """Generate an index page for a specific category (methods, built-ins)."""
    sorted_items = sorted(items.keys(), key=str.lower)
    
    content = f"""# {icon} {title}

Browse all {title.lower()} from your learning logs and concepts.

---

**Total items: {len(sorted_items)}**

"""
    
    for item in sorted_items:
        count = len(items[item])
        display_name = format_name(item)
        content += f"- [{display_name}]({item}.md) — {count} mention{'s' if count != 1 else ''}\n"
    
    content += f"\n---\n\n[← Back to Tag Index](index.md)\n"
    
    return content

def generate_tag_page(tag: str, mentions: List[Tuple], tag_type: str = "tag") -> str:
    """Generate an individual tag page with chronological mentions."""
    # Format the tag display based on type
    if tag_type == "method":
        display_name = f"#{tag}()"
        prefix = "method"
    elif tag_type == "builtin":
        display_name = f"#{tag}()"
        prefix = "built-in function"
    else:
        display_name = f"#{tag}"
        prefix = "tag"
    
    content = f"""# {display_name}

This page shows all mentions of **{display_name}** ({prefix}) across your learning logs and concepts, in chronological order (newest first).

---

"""
    
    content += f"**Total mentions: {len(mentions)}**\n\n"
    
    for file_type, file_path, date, rel_url in mentions:
        icon = "📝" if file_type == "log" else "💡"
        filename = Path(file_path).name
        content += f"{icon} **[{filename}]({rel_url})** — {date}\n"
    
    content += f"\n---\n\n[← Back to Index](index.md)\n"
    
    return content

def create_tag_pages(regular_tags: Dict, methods: Dict, built_ins: Dict) -> None:
    """Create all index and tag pages."""
    # Create tags directory if it doesn't exist
    os.makedirs(TAGS_OUTPUT_DIR, exist_ok=True)
    
    # Generate and write main index
    index_content = generate_tag_index(regular_tags, methods, built_ins)
    index_path = os.path.join(TAGS_OUTPUT_DIR, 'index.md')
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(index_content)
    print(f"✓ Generated {index_path}")
    
    # Generate methods index
    if methods:
        methods_index = generate_index_page(
            "Methods",
            "🔧",
            methods,
            lambda x: f"#{x}()"
        )
        methods_path = os.path.join(TAGS_OUTPUT_DIR, 'methods.md')
        with open(methods_path, 'w', encoding='utf-8') as f:
            f.write(methods_index)
        print(f"✓ Generated {methods_path} ({len(methods)} methods)")
    
    # Generate built-ins index
    if built_ins:
        builtins_index = generate_index_page(
            "Built-in Functions",
            "⚙️",
            built_ins,
            lambda x: f"#{x}()"
        )
        builtins_path = os.path.join(TAGS_OUTPUT_DIR, 'built-ins.md')
        with open(builtins_path, 'w', encoding='utf-8') as f:
            f.write(builtins_index)
        print(f"✓ Generated {builtins_path} ({len(built_ins)} built-ins)")
    
    # Generate individual method pages
    for method, mentions in methods.items():
        tag_page_content = generate_tag_page(method, mentions, "method")
        tag_path = os.path.join(TAGS_OUTPUT_DIR, f'{method}.md')
        with open(tag_path, 'w', encoding='utf-8') as f:
            f.write(tag_page_content)
    
    # Generate individual built-in pages
    for builtin, mentions in built_ins.items():
        tag_page_content = generate_tag_page(builtin, mentions, "builtin")
        tag_path = os.path.join(TAGS_OUTPUT_DIR, f'{builtin}.md')
        with open(tag_path, 'w', encoding='utf-8') as f:
            f.write(tag_page_content)
    
    # Generate individual regular tag pages
    for tag, mentions in regular_tags.items():
        tag_page_content = generate_tag_page(tag, mentions, "tag")
        tag_path = os.path.join(TAGS_OUTPUT_DIR, f'{tag}.md')
        with open(tag_path, 'w', encoding='utf-8') as f:
            f.write(tag_page_content)
        print(f"✓ Generated {tag_path} ({len(mentions)} mentions)")

def main():
    """Main entry point."""
    print("🔍 Scanning for tags in logs and concepts...")
    regular_tags, methods, built_ins = collect_all_mentions()
    
    total = len(regular_tags) + len(methods) + len(built_ins)
    if total == 0:
        print("⚠️  No tags found. Make sure your logs and concepts use:")
        print("   - Regular tags: #tag")
        print("   - Methods: #.method()")
        print("   - Built-ins: #func()")
        return
    
    print(f"📊 Found {len(regular_tags)} regular tags, {len(methods)} methods, {len(built_ins)} built-ins")
    print(f"📍 Generating tag pages in '{TAGS_OUTPUT_DIR}/' directory...")
    
    create_tag_pages(regular_tags, methods, built_ins)
    
    print(f"\n✨ Done! Visit {TAGS_OUTPUT_DIR}/index.md to browse all tags.")

if __name__ == '__main__':
    main()
