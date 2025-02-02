# linter.py

"""
A module for linting and auto-formatting Markdown files prior to conversion
with the Papermill converter. This module uses mdformat to reformat Markdown
and then applies additional linting rules. In this example, we check for table
caption positioning: captions that appear above a table are moved below it,
and an issue is reported.
"""

import re
import mdformat


class MarkdownLinter:
    # Pattern to detect table captions.
    # (e.g., "Table 1:" or "Tab. 2" etc.)
    TABLE_CAPTION_PATTERN = re.compile(r'^(Table|Tab|TABLE|TAB)\.?\s*\d+', re.IGNORECASE)
    # Optionally, a similar pattern can be defined for figure captions if desired.
    FIGURE_CAPTION_PATTERN = re.compile(r'^(Figure|Fig|FIGURE|FIG)\.?\s*\d+', re.IGNORECASE)

    def __init__(self, markdown_text: str):
        """
        Initialize the linter with the Markdown text.
        """
        self.original_text = markdown_text
        self.fixed_text = None
        self.issues = []  # List of tuples: (line number, description)

    def lint(self) -> (list, str):
        """
        Lint and auto-format the Markdown.

        Returns:
            A tuple containing:
            - A list of issues (line number, description)
            - The fixed Markdown text as a single string
        """
        # First, use mdformat to standardize the Markdown.
        formatted_text = mdformat.text(self.original_text)
        lines = formatted_text.splitlines()

        fixed_lines = []
        i = 0
        while i < len(lines):
            line = lines[i]
            stripped_line = line.strip()
            # Check for a table caption line.
            if self.TABLE_CAPTION_PATTERN.match(stripped_line):
                # Look ahead: skip any blank lines.
                j = i + 1
                while j < len(lines) and not lines[j].strip():
                    j += 1
                # If the next non-empty line starts with '|' then this caption is above the table.
                if j < len(lines) and lines[j].strip().startswith("|"):
                    # Report the issue.
                    self.issues.append(
                        (i + 1, "Table caption appears above the table; it should be placed below the table."))
                    # Save the caption and skip it for now.
                    caption_line = line
                    i += 1
                    # Collect the table lines.
                    table_lines = []
                    while i < len(lines) and lines[i].strip().startswith("|"):
                        table_lines.append(lines[i])
                        i += 1
                    # Append the table first, then the caption.
                    fixed_lines.extend(table_lines)
                    fixed_lines.append(caption_line)
                    continue  # Skip the usual line appending.
            # (Additional rules for figure captions or other linting can be inserted here.)
            fixed_lines.append(line)
            i += 1

        self.fixed_text = "\n".join(fixed_lines)
        return self.issues, self.fixed_text