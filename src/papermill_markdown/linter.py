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
    # Pattern to detect table captions (e.g., "Table 1:" or "Tab. 2", etc.)
    TABLE_CAPTION_PATTERN = re.compile(r'^(Table|Tab|TABLE|TAB)\.?\s*\d+', re.IGNORECASE)
    # Pattern for figure captions can be added similarly if needed.
    FIGURE_CAPTION_PATTERN = re.compile(r'^(Figure|Fig|FIGURE|FIG)\.?\s*\d+', re.IGNORECASE)

    def __init__(self, markdown_text: str):
        """
        Initialize the linter with the Markdown text.
        """
        self.original_text = markdown_text
        self.open_issues = []  # List of tuples: (line number, description) for unresolved issues
        self.resolved_issues = []  # List of tuples: (line number, description) for issues fixed automatically
        self.fixed_text = None

    def lint(self) -> (list, list, str):
        """
        Lint and auto-format the Markdown.

        First, mdformat is used to standardize the Markdown.
        Then, the linter scans the text to enforce table caption positioning.
        - If a table caption is found below a table, it is moved above the table.
        Also, each line is checked for an odd number of unescaped "$" signs to detect inline math mismatches.

        Returns:
            A tuple containing:
            - open_issues: a list of (line number, description) for issues that remain.
            - resolved_issues: a list of (line number, description) for issues fixed automatically.
            - fixed_text: the resulting Markdown as a single string.
        """
        # Use mdformat to reformat the original Markdown.
        formatted_text = mdformat.text(self.original_text)
        lines = formatted_text.splitlines()
        fixed_lines = []
        i = 0

        # Process the lines, applying our custom linting rules.
        while i < len(lines):
            line = lines[i]
            stripped = line.strip()

            # Check for table block: if the current line starts with '|' it is part of a table.
            if stripped.startswith("|"):
                # Collect all consecutive table lines.
                table_lines = []
                start_table = i
                while i < len(lines) and lines[i].strip().startswith("|"):
                    table_lines.append(lines[i])
                    i += 1
                # Look ahead for caption below the table.
                j = i
                # Skip blank lines.
                while j < len(lines) and lines[j].strip() == "":
                    j += 1
                if j < len(lines) and self.TABLE_CAPTION_PATTERN.match(lines[j].strip()):
                    # Found a caption below the table; record a resolved issue.
                    self.resolved_issues.append((j + 1, "Table caption moved from below to above the table."))
                    caption_line = lines[j]
                    # Insert the caption above the table.
                    fixed_lines.append(caption_line)
                    fixed_lines.extend(table_lines)
                    # Skip the caption line.
                    i = j + 1
                    continue
                else:
                    # No caption below; output table lines as is.
                    fixed_lines.extend(table_lines)
                    continue

            # For non-table lines, add the line to fixed_lines.
            fixed_lines.append(line)
            i += 1

        # Join the fixed lines back into text.
        self.fixed_text = "\n".join(fixed_lines)

        # Check for unmatched inline math delimiters in each line.
        for idx, line in enumerate(fixed_lines):
            # Count unescaped $ signs.
            dollars = re.findall(r'(?<!\\)\$', line)
            if len(dollars) % 2 != 0:
                self.open_issues.append((idx + 1, "Unmatched inline math delimiter ($) found."))

        return self.open_issues, self.resolved_issues, self.fixed_text