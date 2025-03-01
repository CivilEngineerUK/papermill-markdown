# Papermill Markdown Converter

This repository provides a Python-based solution for converting Markdown documents into a structured JSON payload that conforms to the Papermill API. The converter processes Markdown elements—including headings, paragraphs, inline and block math, code blocks, images, tables, and lists—into the appropriate JSON structure validated by Pydantic.

It is based on the documentation here: [Papermill API Documentation](https://docs.papermill.io/).

## Features

- **Comprehensive Markdown Parsing:**  
  Supports headings (with optional `[ref:identifier]` markers), paragraphs with inline formatting, inline math (using `$...$`), block math (enclosed by standalone `$$` lines), code blocks (using triple backticks), lists (numbered and bullet), images (with captions and optional attributes), and tables.
  
- **Page Breaks:**  
  Inserts page breaks between Markdown sections by use of a triple new line to ensure proper formatting in the generated PDF.

- **Schema Validation:**  
  Uses Pydantic models to ensure the converted JSON adheres to the Papermill API schema.

- **Linter Functionality:**  
  Identifies and resolves issues in the Markdown content, providing feedback on potential problems and automatically correcting some formatting errors.

- **Example Prompt:**  
  Provides a sample prompt (data/prompt.md) that can be given to an LLM to help it to follow a consistent markdown style guide.

- **Structured JSON Output:**  
  *Not tested yet* Use the `DocumentContent` pydantic model to create structured output from an LLM.

- **Papermill API Reference:**  
  Included in `data/papermill_api_reference.txt` is a reference guide for the Papermill API. Note, this is correct as of 02/02/2025 and should be used in conjunction with the official Papermill API documentation.
  *Note:* The Box element is not yet supported in this repo as it is stylistic and more difficult to formalise rules for.

# Installation 

This package is not yet available on PyPI. To install it, clone the repository and install the dependencies using the following commands:

```bash
pip install git+https://github.com/CivilEngineerUK/papermill-markdown
````

# Usage

To convert a Markdown file into JDoc follow this example.:
This assumes that you have a Markdown file (test.md) in the data folder.

```python
import os
from papermill_markdown.converter import MarkdownToPapermill
from papermill_markdown.validator import DocumentContent
from papermill_markdown.linter import MarkdownLinter

# Read the Markdown file
md_filepath = os.path.join('data', 'test.md')  # test file
with open(md_filepath, 'r', encoding='utf-8') as file:
    markdown_original_text = file.read()

# Lint the Markdown file and detail the issues and changes to the file
linter = MarkdownLinter(markdown_original_text)
open_issues, resolved_issues, markdown_text = linter.lint()

# Convert Markdown to Papermill JSON content
converter = MarkdownToPapermill(numbered=True)
papermill_json = converter.convert(markdown_text)

# Validate the entire payload using the DocumentContent model.
document = DocumentContent.model_validate(papermill_json).model_dump()
print(document)
```

You would then insert this into the Papermill API as follows:

```python
{
    "layoutId": "your_layout_id",
    "placeholders": {
        "RecipientName": "John Smith",
        # Add more placeholders here
    },
    "documentContent": document
}
```

Note: You will need a Papermill account to get a layout_id as well as the API key to send this to the API for PDF conversion.

# TODO

1. Fix equations in lists, bold and italics - cannot seem to get this working.
2. Add support for boxes as per [Papermill API Documentation](https://docs.papermill.io/).

# Changelog

- **0.1.10:** 03/02/2025
  - Added support for superscript and subscript including in lists, bold and italics.
- **0.1.11:** 01/03/2025
  - Added support for Base64 encoded images i.e. local images.

# Contributing

Contributions are welcome! Please submit pull requests or open issues for improvements, bug fixes, or new feature suggestions.

# License

This project is licensed under the MIT License. See the LICENSE file for details.