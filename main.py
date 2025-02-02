# data/main.py

import os
import json
import requests
from src.papermill_converter import MarkdownToPapermill
from src.validation_model import PapermillDocument
from dotenv import load_dotenv

def main():
    load_dotenv()

    # get these two from Papermill
    x_api_key = os.getenv("PAPERMILL_API_KEY")
    x_client_id = os.getenv("PAPERMILL_CLIENT_ID")

    url = "https://api.papermill.io/v1/pdf"

    # Load the payload (e.g. letter.json)
    # You will get this from Papermill and will be of the following form:
    """
    # report.json
    {
    "layoutId": "your_layout_id",
    "placeholders": {
        ...
        }
    }
    """

    # see data/json_file/letter_example.json

    json_file_path = 'data/json_file/report.json'
    with open(json_file_path, 'r', encoding='utf-8') as file:
        json_body = json.load(file)

    # Read the Markdown file
    md_filepath = os.path.join('data/test.md') # test file
    with open(md_filepath, 'r', encoding='utf-8') as file:
        markdown_text = file.read()

    # Convert Markdown to Papermill JSON content
    converter = MarkdownToPapermill(numbered=True)
    papermill_json = converter.convert(markdown_text)

    # Insert converted content into the JSON payload
    json_body["documentContent"] = papermill_json

    # Validate the entire payload using the PapermillDocument model.
    # Extra fields (such as placeholders) are allowed.
    document = PapermillDocument.model_validate(json_body)


    # Save the JSON payload with the same name but with a JSON extension
    json_filepath = md_filepath.replace('.md', '.json')
    with open(json_filepath, 'w') as file:
        json.dump(json_body, file, indent=2)

    # Prepare headers
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
        try:
            os.startfile(pdf_path)
        except AttributeError:
            import subprocess
            subprocess.run(["open", pdf_path])
    else:
        print(f"Failed to generate PDF. Status code: {response.status_code}")
        print(response.text)
        print(json.dumps(json_body, indent=2))

if __name__ == "__main__":
    main()
