# Papermill Markdown Converter

This repository provides a Python-based solution for converting Markdown documents into a structured JSON payload that conforms to the Papermill API. The converter processes Markdown elements—including headings, paragraphs, inline and block math, code blocks, images, tables, and lists—into the appropriate JSON structure validated by Pydantic.

It is based on the documentation here: [Papermill API Documentation](https://docs.papermill.io/).

## Features

- **Comprehensive Markdown Parsing:**  
  Supports headings (with optional `[ref:identifier]` markers), paragraphs with inline formatting, inline math (using `$...$`), block math (enclosed by standalone `$$` lines), code blocks (using triple backticks), lists (numbered and bullet), images (with captions and optional attributes), and tables.
  
- **Schema Validation:**  
  Uses Pydantic models to ensure the converted JSON adheres to the Papermill API schema.

- **Example Integration:**  
  Includes an example script to convert a Markdown file and generate a PDF through the Papermill API.

- **Example Prompt:**  
  Provides a sample Markdown file (prompt.md) that follows the Papermill style guide.
- 
# Configuration

Create a `.env` file in the root directory and add your Papermill API credentials:

```bash
PAPERMILL_API_KEY=your_api_key_here
PAPERMILL_CLIENT_ID=your_client_id_here
```

# Usage

To convert a Markdown file and generate a PDF using the Papermill API, run the provided example script:

```bash
python data/main.py
```

The script performs the following steps:

- Reads the sample Markdown file (test_data_1.md).
- Converts the Markdown content into Papermill JSON using the MarkdownToPapermill class.
- Inserts the converted content into a JSON payload (sample payload provided in json_file/letter.json).
- Validates the entire payload using the PapermillDocument model (extra fields, such as placeholders, are allowed).
- Sends a POST request to the Papermill API to generate a PDF.
- Saves the resulting PDF as output.pdf and opens it (if supported by your operating system).

# Example

After configuring your .env file with your API credentials, simply run:

```bash
python data/main.py
```

If successful, you will see the message "PDF generated successfully." and an output.pdf file will be created in the repository directory.

# Contributing

Contributions are welcome! Please submit pull requests or open issues for improvements, bug fixes, or new feature suggestions.

# License

This project is licensed under the MIT License. See the LICENSE file for details.