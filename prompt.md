# Papermill Markdown Style Guide

This document provides succinct guidelines to ensure that your Markdown file is compatible with the Papermill conversion process using the `papermill_converter` class. Follow these instructions exactly.

## 1. Headings

- Use `#` notation for headings.
- Optionally append a reference marker in the format `[ref:identifier]` at the end of the heading text.

## 2. Paragraphs & Inline Formatting

- Write paragraphs as standard text.
- Use inline formatting such as **bold**, *italic*, __underline__, and combined formats as needed.
- Embed inline math expressions using single dollar signs (`$...$`). These will be converted into inline equations.

## 3. Block Math

- Enclose block math with standalone lines containing only `$$` to start and end.
- The content inside will be converted into a block equation element.

## 4. Code Blocks

- Use triple backticks (```) to delimit code blocks.
- An optional language specifier is allowed.

## 5. Lists

- Format numbered lists with digits followed by a period (e.g., `1. Item`).
- Format bullet lists with `-` or `*` at the start of each item.

## 6. Images

- Use the Markdown image syntax:  
  `![Caption](URL "optional attributes")`
- In the title, specify optional attributes as comma-separated key-value pairs (e.g., `ref=identifier, width=40`).

## 7. Tables

- Use standard Markdown table syntax with pipes (`|`) for headers and rows.
- Optionally, include a caption line immediately before or after the table.

## 8. Overall Structure

- Ensure there is no stray text outside of defined block elements.
- All math (inline and block) must be written in standard LaTeX-like notation.

---

By following this style guide, your Markdown will be correctly parsed and converted into Papermill JSON using our converter class.
