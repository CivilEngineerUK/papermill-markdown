# data/example.py



import os
from src.papermill_markdown.converter import MarkdownToPapermill
from src.papermill_markdown.validator import DocumentContent
from src.papermill_markdown.linter import MarkdownLinter

def main():
    # Read the Markdown file
    md_filepath = os.path.join('data/test.md') # test file
    with open(md_filepath, 'r', encoding='utf-8') as file:
        markdown_original_text = file.read()

    # Lint the Markdown file
    linter = MarkdownLinter(markdown_original_text)
    open_issues, resolved_issues, markdown_text = linter.lint()

    # Convert Markdown to Papermill JSON content
    converter = MarkdownToPapermill(numbered=True)
    papermill_json = converter.convert(markdown_text)

    # Validate the entire payload using the PapermillDocument model.
    # Extra fields (such as placeholders) are allowed.
    document = DocumentContent.model_validate(papermill_json).model_dump()
    print(document)


if __name__ == "__main__":
    main()
