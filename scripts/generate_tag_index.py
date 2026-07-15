#!/usr/bin/env python3
"""
Generate tag index and tag-specific pages from markdown files.
Extracts tags in format #tag and creates:
- tags/index.md (master index with all tags)
- tags/tag_name.md (individual pages with chronological mentions)
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
TAG_PATTERN = r'#(\w+)'  # Matches #word (word characters: a-z, A-Z, 0-9, _)

def extract_tags_from_file(file_path: str) -> List[str]:
    """Extract all tags from a markdown file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        tags = re.findall(TAG_PATTERN, content)
        return list(dict.fromkeys(tags))  # Remove duplicates, preserve order
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return []

def get_file_date(file_path: str) -> str:
    """Extract date from file or use modification time."""
    # Try to extract from filename first (format: YYYY-MM-DD-*.md)
    match = re.search(r'(\d{4}-\d{2}-\d{2})', Path(file_path).name)
    if match:
        return match.group(1)
    
    # Fallback to file modification time
    mtime = os.path.getmtime(file_path)
    return datetime.fromtimestamp(mtime).strftime('%Y-%m-%d')

def collect_tag_mentions() -> Dict[str, List[Tuple[str, str, str, str]]]:
    """
    Collect all tag mentions across logs and concepts.
    Returns: {tag: [(file_type, file_path, date, relative_url), ...]}
    """
    tag_mentions = defaultdict(list)
    
    # Process LOGS directory
    if os.path.isdir(LOGS_DIR):
        for filename in sorted(os.listdir(LOGS_DIR)):
            if filename.endswith('.md') and filename != 'logs-template.md':
                file_path = os.path.join(LOGS_DIR, filename)
                tags = extract_tags_from_file(file_path)
                date = get_file_date(file_path)
                rel_url = f"../{file_path}"
                
                for tag in tags:
                    tag_mentions[tag].append(('log', file_path, date, rel_url))
    
    # Process CONCEPTS directory
    if os.path.isdir(CONCEPTS_DIR):
        for filename in sorted(os.listdir(CONCEPTS_DIR)):
            if filename.endswith('.md') and filename != 'concepts-template.md':
                file_path = os.path.join(CONCEPTS_DIR, filename)
                tags = extract_tags_from_file(file_path)
                date = get_file_date(file_path)
                rel_url = f"../{file_path}"
                
                for tag in tags:
                    tag_mentions[tag].append(('concept', file_path, date, rel_url))
    
    # Sort mentions by date (most recent first)
    for tag in tag_mentions:
        tag_mentions[tag].sort(key=lambda x: x[2], reverse=True)
    
    return tag_mentions

def generate_tag_index(tag_mentions: Dict[str, List]) -> str:
    """Generate the main tag index page."""
    # Sort tags alphabetically
    sorted_tags = sorted(tag_mentions.keys(), key=str.lower)
    
    content = """# Tag Index

Browse all tags from your learning logs and concepts. Each tag links to a page showing all chronological mentions.

---

"""
    
    content += f"**Total tags: {len(sorted_tags)}**\n\n"
    
    for tag in sorted_tags:
        count = len(tag_mentions[tag])
        content += f"- [#{tag}]({tag}.md) — {count} mention{'s' if count != 1 else ''}\n"
    
    return content

def generate_tag_page(tag: str, mentions: List[Tuple]) -> str:
    """Generate an individual tag page with chronological mentions."""
    content = f"""# #{tag}

This page shows all mentions of **#{tag}** across your learning logs and concepts, in chronological order (newest first).

---

"""
    
    content += f"**Total mentions: {len(mentions)}**\n\n"
    
    for file_type, file_path, date, rel_url in mentions:
        icon = "📝" if file_type == "log" else "💡"
        # Extract filename for display
        filename = Path(file_path).name
        content += f"{icon} **[{filename}]({rel_url})** — {date}\n"
    
    content += f"\n---\n\n[← Back to Tag Index](index.md)\n"
    
    return content

def create_tag_pages(tag_mentions: Dict[str, List]) -> None:
    """Create tag index and individual tag pages."""
    # Create tags directory if it doesn't exist
    os.makedirs(TAGS_OUTPUT_DIR, exist_ok=True)
    
    # Generate and write index
    index_content = generate_tag_index(tag_mentions)
    index_path = os.path.join(TAGS_OUTPUT_DIR, 'index.md')
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(index_content)
    print(f"✓ Generated {index_path}")
    
    # Generate and write individual tag pages
    for tag, mentions in tag_mentions.items():
        tag_page_content = generate_tag_page(tag, mentions)
        tag_path = os.path.join(TAGS_OUTPUT_DIR, f'{tag}.md')
        with open(tag_path, 'w', encoding='utf-8') as f:
            f.write(tag_page_content)
        print(f"✓ Generated {tag_path} ({len(mentions)} mentions)")

def main():
    """Main entry point."""
    print("🔍 Scanning for tags in logs and concepts...")
    tag_mentions = collect_tag_mentions()
    
    if not tag_mentions:
        print("⚠️  No tags found. Make sure your logs and concepts use the #tag format.")
        return
    
    print(f"📊 Found {len(tag_mentions)} unique tags")
    print(f"📍 Generating tag pages in '{TAGS_OUTPUT_DIR}/' directory...")
    
    create_tag_pages(tag_mentions)
    
    print(f"\n✨ Done! Visit {TAGS_OUTPUT_DIR}/index.md to browse all tags.")

if __name__ == '__main__':
    main()
