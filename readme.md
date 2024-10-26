# Markdown to HTML Converter

A simple Python-based Markdown to HTML converter that supports the following Markdown elements:

- **Headings** (`#`, `##`, `###`, etc.)
- **Bold text** (`**text**`)
- *Italic text* (`*text*`)
- **Links** (`[link text](https://example.com)`)
- **Blockquotes** (`> text`)
- Inline **Code** (`\`code\``)

## Features

This tool parses Markdown syntax and converts it to equivalent HTML. Supported features include:
- Headings converted to `<h1>`, `<h2>`, `<h3>`, etc.
- Bold and italic text styles using `<strong>` and `<em>` tags.
- Links converted to `<a href="...">text</a>` in HTML.
- Blockquotes wrapped with `<blockquote>`.
- Inline code enclosed with `<code>` tags.

## Usage

To use the converter, run the script from the command line, providing the input Markdown file and specifying the output HTML file.

### Example

```bash
python markdown_to_html.py input.md output.html
