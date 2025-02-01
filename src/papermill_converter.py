# src/papermill_converter.py
import re
import unicodedata
import os
import base64
from typing import List, Dict, Union, Tuple, Optional
from urllib.parse import unquote

class MarkdownToPapermill:
    HEADING_PATTERN = re.compile(r'^(#{1,6})\s*(.*)')
    FOOTNOTE_DEF_PATTERN = re.compile(r'\[\^(\d+)\]:\s*([^\n]+)')
    FOOTNOTE_REF_PATTERN = re.compile(r'\[\^(\d+)\]')
    CAPTION_PATTERN = re.compile(r'^(?:Table|Tab|TABLE|TAB)\.?\s*\d+', re.IGNORECASE)
    FIGURE_PATTERN = re.compile(r'^(?:Figure|Fig|FIGURE|FIG)\.?\s*\d+', re.IGNORECASE)
    REFERENCE_SECTION_PATTERNS = [
        re.compile(r'^#{0,6}\s*(References?|Bibliography|Works\s+Cited|Literature(\s+Cited)?|Sources?)$', re.IGNORECASE),
        re.compile(r'^(References?|Bibliography|Works\s+Cited|Literature(\s+Cited)?|Sources?)$', re.IGNORECASE)
    ]
    REFERENCE_LINE_PATTERNS = [
        re.compile(r'^\s*\[?\d+[\]\.]'),
        re.compile(r'^\s*\([A-Z][a-zA-Z\s,\.-]+,?\s*\d{4}\)'),
        re.compile(r'^\s*[A-Z][a-zA-Z\s,\.-]+\s*\(\d{4}\)'),
        re.compile(r'^\s*\[[A-Z][a-zA-Z\s,\.-]+(?:\s+et\s+al\.?)?,?\s*\d{4}\]')
    ]
    LIST_ITEM_PATTERN = re.compile(r'^(\d+\.)|^([-*])\s+')

    # Patterns for inline formatting
    INLINE_FORMATTING_PATTERNS = {
        'bold_italic': re.compile(r'\*\*\*(.+?)\*\*\*'),
        'bold': re.compile(r'\*\*(.+?)\*\*'),
        'italic': re.compile(r'(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)'),
        'underline': re.compile(r'__(.+?)__'),
        'superscript_md': re.compile(r'\^(.+?)\^'),
        'subscript_md': re.compile(r'~(.+?)~'),
        'superscript_html': re.compile(r'<sup>(.+?)<\/sup>'),
        'subscript_html': re.compile(r'<sub>(.+?)<\/sub>'),
        'cross_ref': re.compile(r'\[ref:(.+?)\]'),
        'hyperlink': re.compile(r'\[(?!\^|ref:)(.+?)\]\((.+?)\)'),
        # We will handle inline math separately using a custom method
    }

    # Block math patterns
    BLOCK_MATH_START_PATTERN = re.compile(r'^\$\$\s*$')
    BLOCK_MATH_END_PATTERN = re.compile(r'^\$\$\s*$')

    # Inline math pattern
    # We'll find all `$...$` expressions line by line
    INLINE_MATH_PATTERN = re.compile(r'\$(.+?)\$')

    def __init__(self, numbered: bool = True):
        self.footnotes = {}
        self.numbered = numbered

    def convert(self, markdown_text: str) -> List[Dict]:
        # Normalize and fix encoding issues
        markdown_text = unicodedata.normalize('NFC', markdown_text)
        replacements = {
            'Â£': '£',
            'â€”': '—',
            'â€“': '–',
            'â€™': '’',
            'â€˜': '‘',
            'â€œ': '“',
            'â€�': '”',
            'â€¦': '…'
        }
        for k, v in replacements.items():
            markdown_text = markdown_text.replace(k, v)

        # Extract footnotes
        markdown_text, self.footnotes = self._process_footnotes(markdown_text)

        lines = markdown_text.split('\n')
        result = []
        buffer = []
        skip_lines = set()

        # Identify caption lines to skip
        for idx, line in enumerate(lines):
            line = line.strip()
            if self.CAPTION_PATTERN.match(line) or self.FIGURE_PATTERN.match(line):
                skip_lines.add(idx)

        i = 0
        while i < len(lines):
            line = lines[i].strip()

            # Handle block math start
            if self.BLOCK_MATH_START_PATTERN.match(line):
                # Finish current paragraph before math block
                if buffer:
                    result.append(self._process_paragraph(' '.join(buffer)))
                    buffer = []
                i += 1
                block_math_content = []
                while i < len(lines) and not self.BLOCK_MATH_END_PATTERN.match(lines[i].strip()):
                    block_math_content.append(lines[i])
                    i += 1
                i += 1  # skip the closing $$
                math_text = '\n'.join(block_math_content).strip()
                if math_text:
                    # Add math block as a separate object
                    result.append({"type": "math", "text": math_text})
                continue

            # Skip caption lines
            if i in skip_lines:
                i += 1
                continue

            # Check if reference section
            if self._is_reference_section_heading(line):
                if buffer:
                    result.append(self._process_paragraph(' '.join(buffer)))
                    buffer = []
                heading = self._process_heading(line if line.startswith('#') else f'## {line}')
                result.append(heading)
                i += 1
                # Skip blank lines
                while i < len(lines) and not lines[i].strip():
                    i += 1
                # Process references
                while i < len(lines):
                    ref_line = lines[i].strip()
                    if not ref_line or ref_line.startswith('#'):
                        break
                    if self._is_reference_line(ref_line):
                        result.append({
                            "type": "paragraph",
                            "text": [ref_line]
                        })
                    i += 1
                continue

            # If empty line, paragraph break
            if not line:
                if buffer:
                    result.append(self._process_paragraph(' '.join(buffer)))
                    buffer = []
                i += 1
                continue

            # Headings
            heading_match = self.HEADING_PATTERN.match(line)
            if heading_match:
                if buffer:
                    result.append(self._process_paragraph(' '.join(buffer)))
                    buffer = []
                heading = self._process_heading(line)
                result.append(heading)
                i += 1
                continue

            # Lists
            if self.LIST_ITEM_PATTERN.match(line):
                if buffer:
                    result.append(self._process_paragraph(' '.join(buffer)))
                    buffer = []
                i = self._process_list(lines, i, result)
                continue

            # Images
            if line.startswith('!['):
                if buffer:
                    result.append(self._process_paragraph(' '.join(buffer)))
                    buffer = []
                image_dict, i = self._process_image(line, lines, i)
                result.append(image_dict)
                continue

            # Tables
            if line.startswith('|'):
                if buffer:
                    result.append(self._process_paragraph(' '.join(buffer)))
                    buffer = []
                i = self._process_table(lines, i, result)
                continue

            # Regular text line
            buffer.append(line)
            i += 1

        # Final paragraph if buffer not empty
        if buffer:
            result.append(self._process_paragraph(' '.join(buffer)))

        return result

    def _process_heading(self, line: str) -> Dict:
        match = self.HEADING_PATTERN.match(line)
        if not match:
            return {}
        hashes, text = match.groups()
        level = min(len(hashes), 5)
        return {
            "type": "heading",
            "text": text.strip(),
            "level": level,
            "numbered": self.numbered
        }

    def _process_list(self, lines: List[str], start_idx: int, result: List) -> int:
        items = []
        i = start_idx
        first_line = lines[i].strip()
        is_numbered = first_line and first_line[0].isdigit()

        while i < len(lines):
            line = lines[i].strip()
            if not line:
                break
            match = self.LIST_ITEM_PATTERN.match(line)
            if match:
                if is_numbered and match.group(1):
                    text = line[line.find('.') + 1:].strip()
                elif not is_numbered and match.group(2):
                    text = line[2:].strip()
                else:
                    break
                item_tokens = self._process_inline_formatting(text)
                if isinstance(item_tokens, list):
                    items.append(item_tokens)
                else:
                    items.append([item_tokens])
                i += 1
            else:
                break

        result.append({
            "type": "list",
            "style": "number" if is_numbered else "bullet",
            "items": items
        })
        return i

    def _clean_caption_text(self, raw_caption: str) -> str:
        if not raw_caption:
            return ""
        match = re.match(r'^(?:Table|Tab|TABLE|TAB|Figure|Fig|FIGURE|FIG)\.?\s*\d+(?:\.\d+)*\s*[-:~]?\s*(.*)', raw_caption, re.IGNORECASE)
        if match:
            return match.group(1).strip()
        return raw_caption.strip()

    def _find_caption(self, lines: List[str], start_idx: int, prefix_patterns: List[str]) -> Tuple[Optional[str], int]:
        # Look before content
        for idx in range(max(0, start_idx - 2), start_idx):
            line = lines[idx].strip()
            for pattern in prefix_patterns:
                if re.match(f'^{pattern}\.?\s*\d+', line, re.IGNORECASE):
                    return self._clean_caption_text(line), start_idx

        # Look after content
        for idx in range(start_idx + 1, min(len(lines), start_idx + 3)):
            line = lines[idx].strip()
            for pattern in prefix_patterns:
                if re.match(f'^{pattern}\.?\s*\d+', line, re.IGNORECASE):
                    return self._clean_caption_text(line), idx + 1

        return None, start_idx

    def _process_table(self, lines: List[str], start_idx: int, result: List) -> int:
        caption, i = self._find_caption(lines, start_idx, ['Table', 'Tab', 'TABLE', 'TAB'])

        if i >= len(lines) or not lines[i].strip().startswith('|'):
            return i

        # Header
        header_line = lines[i].strip()
        header_cells = [cell.strip() for cell in header_line.split('|')[1:-1]]
        i += 1

        # Separator line
        if i < len(lines) and re.match(r'^\|(?:\s*[-:]+\s*\|)+', lines[i].strip()):
            i += 1

        # Body
        body = []
        while i < len(lines):
            line = lines[i].strip()
            if not line.startswith('|'):
                break
            cells = [cell.strip() for cell in line.split('|')[1:-1]]
            body.append(cells)
            i += 1

        if not caption:
            caption, i = self._find_caption(lines, i, ['Table', 'Tab', 'TABLE', 'TAB'])

        table_obj = {
            "type": "table",
            "header": header_cells,
            "body": body,
            "caption": caption or ""
        }
        result.append(table_obj)
        return i

    def _process_image(self, line: str, lines: List[str], current_idx: int) -> Tuple[Dict, int]:
        alt_text_match = re.search(r'!\[(.*?)\]', line)
        url_title_match = re.search(r'\((.*?)\)', line)

        image_obj = {"type": "image"}

        if not alt_text_match or not url_title_match:
            return image_obj, current_idx + 1

        alt_text = alt_text_match.group(1).strip()
        url_title = url_title_match.group(1).strip()

        # Extract possible title
        title_match = re.search(r'^(.*?)\s+"(.*?)"$', url_title)
        if title_match:
            image_url = title_match.group(1).strip()
            title_str = title_match.group(2).strip()
        else:
            image_url = url_title
            title_str = None

        image_url = self._handle_image_url(image_url)
        image_obj["url"] = image_url

        if alt_text:
            image_obj["caption"] = [alt_text]

        if title_str:
            attrs = [attr.strip() for attr in title_str.split(',')]
            for attr in attrs:
                if '=' in attr:
                    k, v = attr.split('=', 1)
                    k = k.strip()
                    v = v.strip()
                    if k == 'caption':
                        image_obj['caption'] = [v]
                    elif k == 'ref':
                        image_obj['ref'] = v
                    elif k == 'width':
                        image_obj['width'] = v
                else:
                    if attr == 'fullWidth':
                        image_obj['fullWidth'] = True

        return image_obj, current_idx + 1

    def _handle_image_url(self, image_url: str) -> str:
        if image_url.startswith('http') or image_url.startswith('data:image/'):
            return image_url

        local_path = unquote(image_url)
        if os.path.exists(local_path) and os.path.isfile(local_path):
            ext = os.path.splitext(local_path.lower())[1]
            if ext in ['.png']:
                mime = 'image/png'
            elif ext in ['.jpg', '.jpeg']:
                mime = 'image/jpeg'
            elif ext in ['.gif']:
                mime = 'image/gif'
            else:
                mime = 'image/png'

            with open(local_path, 'rb') as f:
                data = f.read()
            b64 = base64.b64encode(data).decode('utf-8')
            return f"data:{mime};base64,{b64}"
        else:
            # File not found locally, return as-is
            return image_url

    def _process_footnotes(self, text: str) -> Tuple[str, Dict[str, str]]:
        footnotes = {}
        def replace_definition(m):
            footnote_id, content = m.groups()
            footnotes[footnote_id] = content.strip()
            return ''
        text = self.FOOTNOTE_DEF_PATTERN.sub(replace_definition, text)
        text = self.FOOTNOTE_REF_PATTERN.sub(lambda m: f"__FOOTNOTE__{m.group(1)}__", text)
        return text, footnotes

    def _process_paragraph(self, text: str) -> Dict:
        if not text:
            return {"type": "paragraph", "text": []}

        # Handle footnotes first
        parts = text.split('__FOOTNOTE__')
        result = []
        for part in parts:
            if '__' in part:
                footnote_id, remaining = part.split('__', 1)
                if part.startswith('CROSS_REF__'):
                    _, ref_id = footnote_id.split('__')
                    result.append({"type": "crossReference", "ref": ref_id, "label": self._get_reference_label(ref_id)})
                elif part.startswith('HYPERLINK__'):
                    link_text, url = remaining.split('__URL__', 1)
                    result.append({"url": url, "text": link_text})
                elif part.startswith('INLINE_MATH__'):
                    math_text = footnote_id[len('INLINE_MATH__'):]
                    result.append({"type": "math", "text": math_text})
                else:
                    result.append({"type": "footnote", "text": self.footnotes.get(footnote_id, "")})
            else:
                # Process inline formatting including inline math
                formatted = self._process_inline_math_and_formatting(part.strip())
                if isinstance(formatted, list):
                    result.extend(formatted)
                else:
                    if formatted:
                        result.append(formatted)

        return {"type": "paragraph", "text": result if result else [""]}

    def _process_inline_math_and_formatting(self, text: str) -> Union[str, List]:
        # Extract inline math segments
        # We'll split the text by inline math tokens and reinsert as needed
        segments = []
        last_pos = 0

        for m in self.INLINE_MATH_PATTERN.finditer(text):
            # text before math
            if m.start() > last_pos:
                before = text[last_pos:m.start()]
                segments.append(self._process_inline_formatting(before))
            # math content
            math_content = m.group(1).strip()
            segments.append({"type": "math", "text": math_content})
            last_pos = m.end()

        # trailing text after last math
        if last_pos < len(text):
            trailing = text[last_pos:]
            segments.append(self._process_inline_formatting(trailing))

        # Flatten segments
        flattened = []
        for seg in segments:
            if isinstance(seg, list):
                flattened.extend(seg)
            elif seg:
                flattened.append(seg)

        return flattened if len(flattened) > 1 else (flattened[0] if flattened else "")

    def _process_inline_formatting(self, text: str) -> Union[str, List]:
        if not text:
            return text

        # First handle cross_references and hyperlinks already done in _process_paragraph?
        # They are done there, so we only handle bold/italic etc here.

        tokens = []
        pos = 0
        # Apply formatting patterns
        while pos < len(text):
            match_found = False
            # Check standard formatting patterns
            for fmt, pattern in self.INLINE_FORMATTING_PATTERNS.items():
                m = pattern.search(text, pos)
                if m and m.start() == pos:
                    val = m.group(1)
                    token = {"text": val}
                    if fmt == 'bold_italic':
                        token['bold'] = True
                        token['italic'] = True
                    elif fmt == 'bold':
                        token['bold'] = True
                    elif fmt == 'italic':
                        token['italic'] = True
                    elif fmt == 'underline':
                        token['underline'] = True
                    elif fmt in ['superscript_md', 'superscript_html']:
                        token['superscript'] = True
                    elif fmt in ['subscript_md', 'subscript_html']:
                        token['subscript'] = True
                    tokens.append(token)
                    pos = m.end()
                    match_found = True
                    break
            if not match_found:
                # No formatting match at this position, find next formatting start
                next_positions = []
                for pat in self.INLINE_FORMATTING_PATTERNS.values():
                    nm = pat.search(text, pos)
                    if nm:
                        next_positions.append(nm.start())
                next_pos = min(next_positions) if next_positions else len(text)
                tokens.append(text[pos:next_pos])
                pos = next_pos

        tokens = [t for t in tokens if t != '']  # Remove empty tokens
        return tokens if len(tokens) > 1 else (tokens[0] if tokens else "")

    def _get_reference_label(self, ref_id: str) -> str:
        if ref_id.startswith('fig-'):
            return "figure"
        elif ref_id.startswith('tbl-'):
            return "table"
        else:
            return "section"

    def _is_reference_section_heading(self, line: str) -> bool:
        return any(pattern.match(line) for pattern in self.REFERENCE_SECTION_PATTERNS)

    def _is_reference_line(self, line: str) -> bool:
        return any(pattern.match(line) for pattern in self.REFERENCE_LINE_PATTERNS)
