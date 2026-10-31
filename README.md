# markparse

![Python](https://img.shields.io/badge/python-3.10+-blue.svg)
![Tests](https://github.com/amelfia/markparse/actions/workflows/test.yml/badge.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Dependencies](https://img.shields.io/badge/dependencies-none-orange.svg)

A zero-dependency Markdown-to-HTML compiler and static site generator in Python. It parses Markdown into an AST of HTML nodes and renders each page into a shared HTML template.

**Live demo:** https://amelfia.github.io/markparse/ (my own site, built with markparse)

## Motivation

I wanted to push my skill set past everyday scripting and into how compilers actually work: tokenizing raw text, building a tree, and turning that tree back into output. Markdown was a good target because the input is simple but the edge cases are not. I built markparse with zero dependencies so every step, from raw `.md` to a finished HTML page, is code I wrote and understand. Now I use it to build my own site, and when my pages needed something the parser couldn't do, like code blocks with a language tag, I added it.

---

## How it works

The pipeline, standard library only:

```text
[content/*.md] ──► Block Classifier ──► AST Generator (ParentNode / LeafNode)
                          │                              │
                          ▼                              ▼
                  Inline Tokenizer               HTML Serialization
                (Regex & Delimiters)                     │
                                                         ▼
[template.html] ───────────────────────────────► Template fill ──► [docs/*.html]
```

1. **Inline Tokenization:** Parses raw text into `TextNode` objects by splitting on delimiters (`**`, `_`, `` ` ``) and using regular expressions for links and images.
2. **Block Parsing:** Classifies each block (headings, paragraphs, blockquotes, unordered/ordered lists, code blocks) by its prefix into a `BlockType` enum.
3. **AST Composition:** Builds a tree of `ParentNode` and `LeafNode` instances (Composite pattern), which serializes itself to HTML recursively.
4. **Site Compilation:** Walks `content/` recursively and mirrors its folders into `docs/`, copies `static/` across, fills `template.html` with each page's title and HTML, then prefixes root-relative links with the basepath.

## Features

- **Zero third-party dependencies:** standard library only (`re`, `os`, `sys`, `enum`, `shutil`, `pathlib`, `unittest`)
- **Supported Markdown:**
  - Headings (`#` to `######`)
  - Paragraphs (lines joined into one)
  - Lists: `- item` and `1. item` (numbered 1, 2, 3… in order)
  - Fenced code blocks (a language tag after the backticks is allowed and ignored)
  - Blockquotes (`>`)
  - Images `![alt](src)` and links `[text](url)`
  - `**bold**`, `_italic_` and `` `code` ``

- **Not supported yet:**
  - nested formatting, `*italic*`, `* ` lists, nested lists, tables, blank lines inside code blocks, and HTML escaping (anything that looks like a tag, such as `<name>`, is read as HTML, even inside a code block). A lone `_` or backtick (e.g. `snake_case`) raises an "unmatched" error.
  - **Basepath routing:** set via a CLI argument for hosting under a sub-path (e.g. GitHub Pages)
  - **Asset sync:** clears `docs/` and copies `static/` into it on every build

## Quick Start

### Prerequisites

- Python 3.10+

### Run it

```bash
git clone https://github.com/amelfia/markparse.git
cd markparse
./main.sh
```

`main.sh` builds the site into `docs/` and serves it at <http://localhost:8888>.

## Usage

### Writing pages

- Every `.md` file in `content/` becomes a page, and folders become URLs: `content/blog/post/index.md` → `/blog/post/`.
- Every page needs a `# Title` line. It fills `{{ Title }}` in `template.html`, and the build stops if it's missing.
- Files in `static/` (CSS, images) are copied into `docs/` as they are.

### Building for GitHub Pages

```bash
./build.sh
# Or directly:
python3 src/main.py "/markparse/"
```

This rewrites `href="/` and `src="/` links to start with `/markparse/`, so the site works from the repo's Pages URL.

## Contributing

### Run the test suite

48 unittest cases covering tokenization, block parsing, HTML rendering and title extraction. GitHub Actions runs them on every push.

```bash
./test.sh
```

### Submit a pull request

Fork the repository and open a pull request.
