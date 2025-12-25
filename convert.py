#!/usr/bin/env python3
"""
Simple Markdown to HTML converter for blog posts.
Usage: python3 convert.py blogs/gpus/example-post.md
"""

import re
import sys
from pathlib import Path

def parse_frontmatter(content):
    """Extract YAML frontmatter from markdown."""
    match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
    if match:
        frontmatter = {}
        for line in match.group(1).strip().split('\n'):
            if ':' in line:
                key, value = line.split(':', 1)
                frontmatter[key.strip()] = value.strip()
        remaining = content[match.end():]
        return frontmatter, remaining
    return {}, content

def markdown_to_html(md_text):
    """Convert markdown to HTML (basic implementation)."""
    html = md_text

    # Headers
    html = re.sub(r'^### (.*?)$', r'<h3 id="\1">\1</h3>', html, flags=re.MULTILINE)
    html = re.sub(r'^## (.*?)$', lambda m: f'<h2 id="{m.group(1).lower().replace(" ", "-")}">{m.group(1)}</h2>', html, flags=re.MULTILINE)
    html = re.sub(r'^# (.*?)$', r'<h1>\1</h1>', html, flags=re.MULTILINE)

    # Bold
    html = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', html)

    # Code
    html = re.sub(r'`([^`]+)`', r'<code>\1</code>', html)

    # Links
    html = re.sub(r'\[([^\]]+)\]\(([^\)]+)\)', r'<a href="\2">\1</a>', html)

    # Lists
    lines = html.split('\n')
    in_list = False
    result = []
    for line in lines:
        if re.match(r'^- ', line):
            if not in_list:
                result.append('<ul>')
                in_list = True
            result.append(f'<li>{line[2:]}</li>')
        elif re.match(r'^\d+\. ', line):
            if not in_list:
                result.append('<ol>')
                in_list = True
            result.append(f'<li>{re.sub(r"^\d+\. ", "", line)}</li>')
        else:
            if in_list:
                result.append('</ul>' if result[-1].startswith('<li>') else '</ol>')
                in_list = False
            result.append(line)

    if in_list:
        result.append('</ul>')

    html = '\n'.join(result)

    # Paragraphs (simple approach)
    html = re.sub(r'\n\n+', '</p>\n\n<p>', html)
    html = '<p>' + html + '</p>'
    html = re.sub(r'<p>\s*<(h[123]|ul|ol)', r'<\1', html)
    html = re.sub(r'</(h[123]|ul|ol)>\s*</p>', r'</\1>', html)
    html = re.sub(r'<p>\s*</p>', '', html)

    return html

def generate_toc(content):
    """Generate table of contents from headers."""
    headers = re.findall(r'^## (.*?)$', content, re.MULTILINE)
    if not headers:
        return ''

    toc_items = []
    for header in headers:
        anchor = header.lower().replace(' ', '-')
        toc_items.append(f'<li><a href="#{anchor}">{header}</a></li>')

    return f'''
            <div class="toc collapsed" id="toc">
                <div class="toc-header" onclick="toggleTOC()">
                    <span class="toc-arrow">▶</span>
                    <span>Table of contents</span>
                </div>
                <div class="toc-content">
                    <ul>
                        {chr(10).join(toc_items)}
                    </ul>
                </div>
            </div>
'''

def create_html_page(frontmatter, content_html, toc_html):
    """Generate complete HTML page."""
    title = frontmatter.get('title', 'Untitled Post')
    date = frontmatter.get('date', '')
    tags = frontmatter.get('tags', '')
    author = frontmatter.get('author', 'satvik')

    template = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} - satvik</title>
    <link rel="stylesheet" href="../../styles.css">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600&display=swap" rel="stylesheet">
</head>
<body>
    <div class="banner">
        <div class="banner-content">
            <h1 class="banner-title">satvik</h1>
        </div>
    </div>

    <main class="container">
        <nav class="breadcrumb">
            <a href="../../index.html">satvik</a> / <a href="../../index.html">blogs</a> / <a href="../index.html">gpus</a> / {title}
        </nav>

        <article>
            <header class="post-header">
                <h1 class="post-title">{title}</h1>
                <div class="post-author">by <a href="../../index.html">{author}</a></div>
                <div class="post-meta">
                    <span class="date">{date}</span>
                    <span class="tags">{tags}</span>
                </div>
            </header>

{toc_html}

            <div class="post-content">
                {content_html}

                <a href="../../index.html" class="back-link">← Back to blogs</a>
            </div>
        </article>
    </main>

    <footer>
        <p>© 2025 satvik</p>
    </footer>

    <script src="../../script.js"></script>
</body>
</html>
'''
    return template

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 convert.py <markdown-file>")
        sys.exit(1)

    md_file = Path(sys.argv[1])
    if not md_file.exists():
        print(f"Error: File {md_file} not found")
        sys.exit(1)

    # Read markdown file
    md_content = md_file.read_text()

    # Parse frontmatter and content
    frontmatter, content = parse_frontmatter(md_content)

    # Convert markdown to HTML
    content_html = markdown_to_html(content)

    # Generate TOC
    toc_html = generate_toc(content)

    # Create full HTML page
    html = create_html_page(frontmatter, content_html, toc_html)

    # Write HTML file
    html_file = md_file.with_suffix('.html')
    html_file.write_text(html)

    print(f"✓ Converted {md_file} → {html_file}")

if __name__ == "__main__":
    main()
