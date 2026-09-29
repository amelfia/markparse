# markparse

![Python](https://img.shields.io/badge/python-3.10+-blue.svg)
![Tests](https://github.com/amelfia/markparse/actions/workflows/test.yml/badge.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Dependencies](https://img.shields.io/badge/dependencies-none-orange.svg)

A zero-dependency Markdown-to-HTML AST compiler and static site generator written in Python.

`markparse` tokenizes Markdown into a custom HTML Abstract Syntax Tree (AST), validates inline formatting and block structures, and recursively compiles document trees against HTML layout templates.

---

## Overview & Architecture

`markparse` implements an AST-based lexer and compiler pipeline from scratch using only the Python standard library:

```text
[content/*.md] ──► Block Classifier ──► AST Generator (ParentNode / LeafNode)
                          │                              │
                          ▼                              ▼
                  Inline Tokenizer               HTML Serialization
                (Regex & Delimiters)                     │
                                                         ▼
[template.html] ───────────────────────────────► Template Engine ──► [docs/*.html]
```

1. **Inline Tokenization:** Parses raw text into `TextNode` objects by evaluating delimiters (`**`, `_`, `` ` ``) and regular expressions for links and images.
2. **Block Parsing:** Classifies structural sections (headings, paragraphs, blockquotes, unordered/ordered lists, code blocks) into distinct `BlockType` enums.
3. **AST Composition:** Constructs a hierarchical DOM tree using composite `ParentNode` and `LeafNode` instances.
4. **Site Compilation:** Scans directory trees recursively, mirrors directory hierarchies, copies static assets (images, CSS), and injects rendered HTML into target templates with custom basepath routing.

## Features

- **Zero third-party dependencies:** relies purely on the Python standard library (`re`, `os`, `shutil`, `pathlib`, `unittest`)
- **Comprehensive Markdown support:**
  - Headings (`h1` through `h6`)
  - Paragraphs and multi-line text folding
  - Unordered and ordered lists
  - Code blocks (`<pre><code>`)
  - Blockquotes (`<blockquote>`)
  - Inline images and hyperlinks
  - Formatted text: bold, italic, code
- **Basepath routing:** configurable via CLI argument for hosting under custom sub-paths (e.g. GitHub Pages)
- **Automated asset sync:** cleans and mirrors static assets (stylesheets, images) on build

## Getting Started

### Prerequisites

- Python 3.10+

### Installation

```bash
git clone https://github.com/amelfia/markparse.git
cd markparse
```

### Building the Site

Compile with the default basepath (`/`):

```bash
python3 src/main.py
```

Compile for GitHub Pages deployment:

```bash
./build.sh
# Or directly:
python3 src/main.py "/markparse/"
```

Compiled pages and assets are written to `./docs`.

### Local Preview

Serve the generated site with Python's built-in HTTP server:

```bash
cd docs && python3 -m http.server 8888
```

Then open <http://localhost:8888> in your browser.

## Running Tests

Run the full unit test suite covering tokenization, block parsing, HTML tree rendering, and title extraction:

```bash
./test.sh
```
