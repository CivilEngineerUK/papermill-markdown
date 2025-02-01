# tests/test_create_pdf.py

import os
import json
import requests
from src.papermill_converter import MarkdownToPapermill
from src.validation_model import PapermillDocument, DocumentContent
from dotenv import load_dotenv

def main():
    load_dotenv()

    x_api_key = os.getenv("PAPERMILL_API_KEY")
    x_client_id = os.getenv("PAPERMILL_CLIENT_ID")
    url = "https://api.papermill.io/v1/pdf"

    # Choose the JSON payload (e.g. letter.json)
    json_file_path = os.path.join('json_file', 'letter.json')
    with open(json_file_path, 'r', encoding='utf-8') as file:
        json_body = json.load(file)

    # Read the Markdown file
    md_filepath = os.path.join('test_data_1.md')
    with open(md_filepath, 'r', encoding='utf-8') as file:
        markdown_text = file.read()

    # Convert Markdown to Papermill JSON
    converter = MarkdownToPapermill(numbered=False)
    papermill_json = converter.convert(markdown_text)

    # Insert converted content into the JSON payload
    json_body["documentContent"] = papermill_json

    # Validate the document content (using Pydantic)
    validated_body = DocumentContent.model_validate({"documentContent": papermill_json})
    document = PapermillDocument.model_validate(json_body)

    # Prepare headers (note: content type must be "application/json")
    headers = {
        "x-api-key": x_api_key,
        "x-client-id": x_client_id,
        "Content-Type": "application/json"
    }

    response = requests.post(url, json=json_body, headers=headers)

    if response.status_code == 200:
        pdf_path = "output.pdf"
        with open(pdf_path, "wb") as f:
            f.write(response.content)
        print("PDF generated successfully.")
        # Open the PDF with the default viewer (Windows only; adjust for your OS as needed)
        try:
            os.startfile(pdf_path)
        except AttributeError:
            # For non-Windows platforms, you may use an alternative method
            import subprocess
            subprocess.run(["open", pdf_path])
    else:
        print(f"Failed to generate PDF. Status code: {response.status_code}")
        print(response.text)
        print(json.dumps(json_body, indent=2))

if __name__ == "__main__":
    main()
