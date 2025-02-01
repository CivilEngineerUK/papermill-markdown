# tests/test_create_pdf.py

from src.papermill_converter import MarkdownToPapermill
import requests
import os
import json
from src.validation_model import PapermillDocument, DocumentContent
from dotenv import load_dotenv
load_dotenv()


x_api_key = os.getenv("PAPERMILL_API_KEY")
x_client_id = os.getenv("PAPERMILL_CLIENT_ID")
url = "https://api.papermill.io/v1/pdf"


json_file_path = 'json_file/report.json' # these are your specific payloads
json_file_path = 'json_file/letter.json'

with open(json_file_path, 'r') as file:
    json_body = json.load(file)

# read test.md
filepath = 'test_data_1.md'
with open(filepath, 'r', encoding ='utf-8') as file:
    markdown_text = file.read()

converter = MarkdownToPapermill(False)

papermill_json = converter.convert(markdown_text)

json_body["documentContent"] = papermill_json

validated_body = DocumentContent.model_validate({"documentContent": papermill_json})
document = PapermillDocument.model_validate(json_body)


headers = {
    "x-api-key": x_api_key,
    "x-client-id": x_client_id,
    "Content-Type": "application/json_file"
}

response = requests.post(url, json=json_body, headers=headers)

if response.status_code == 200:
    pdf_path = "output.pdf"
    with open(pdf_path, "wb") as f:
        f.write(response.content)
    print("PDF generated successfully.")
    os.startfile(pdf_path)  # This will open the PDF with the default viewer on Windows
else:
    print(f"Failed to generate PDF. Status code: {response.status_code}")
    print(response.text)
    print(json.dumps(json_body, indent=2))