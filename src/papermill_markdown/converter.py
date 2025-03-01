# src/papermill_markdown/converter.py

import re
import unicodedata
import os
import base64
from typing import List, Dict, Union, Tuple, Optional
from urllib.parse import unquote


class MarkdownToPapermill:
    # Regular expression patterns
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
        # Bold + italic
        'bold_italic': re.compile(r'\*\*\*(.+?)\*\*\*'),
        # Bold
        'bold': re.compile(r'\*\*(.+?)\*\*'),
        # Italic
        'italic': re.compile(r'(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)'),
        # Underline
        'underline': re.compile(r'__(.+?)__'),
        # Superscript
        'superscript_md': re.compile(r'\^(.+?)\^'),
        'superscript_html': re.compile(r'<sup>(.+?)<\/sup>'),
        # Subscript
        'subscript_md': re.compile(r'~(.+?)~'),
        'subscript_html': re.compile(r'<sub>(.+?)<\/sub>'),
        # Hyperlink
        'hyperlink': re.compile(r'\[(?!\^|ref:)(.+?)\]\((.+?)\)')
    }

    # NEW/UPDATED: single pattern for either crossReference or reference
    #   If label= is present, treat as crossReference; otherwise treat as reference.
    REF_PATTERN = re.compile(r'\[ref:(?P<ref>[^\]\s]+)(?:\s+label=(?P<label>[^\]]+))?\]')

    # Math patterns
    BLOCK_MATH_START_PATTERN = re.compile(r'^\$\$\s*$')
    BLOCK_MATH_END_PATTERN = re.compile(r'^\$\$\s*$')
    INLINE_MATH_PATTERN = re.compile(r'\$(.+?)\$')

    def __init__(self, numbered: bool = True):
        self.footnotes = {}
        self.numbered = numbered

    def convert(self, markdown_text: str) -> List[Dict]:
        # Normalize Unicode and apply simple replacements.
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

        # Process footnotes
        markdown_text, self.footnotes = self._process_footnotes(markdown_text)
        lines = markdown_text.split('\n')
        result = []
        buffer = []
        skip_lines = set()

        # Identify lines that look like captions and skip them
        for idx, line in enumerate(lines):
            if self.CAPTION_PATTERN.match(line.strip()) or self.FIGURE_PATTERN.match(line.strip()):
                skip_lines.add(idx)

        empty_count = 0
        i = 0
        while i < len(lines):
            line = lines[i].strip()

            # Block math
            if self.BLOCK_MATH_START_PATTERN.match(line):
                if buffer:
                    result.append(self._process_paragraph(" ".join(buffer)))
                    buffer = []
                i += 1
                block_lines = []
                while i < len(lines) and not self.BLOCK_MATH_END_PATTERN.match(lines[i].strip()):
                    block_lines.append(lines[i])
                    i += 1
                i += 1  # skip the closing $$
                eq_text = "\n".join(block_lines).strip()
                if eq_text:
                    result.append({"type": "equation", "equation": eq_text})
                empty_count = 0
                continue

            # Code blocks
            if line.startswith("```"):
                if buffer:
                    result.append(self._process_paragraph(" ".join(buffer)))
                    buffer = []
                i += 1
                code_lines = []
                while i < len(lines) and not lines[i].strip().startswith("```"):
                    code_lines.append(lines[i])
                    i += 1
                i += 1  # skip closing ```
                result.append({"type": "code", "text": "\n".join(code_lines)})
                empty_count = 0
                continue

            # Skip caption lines
            if i in skip_lines:
                i += 1
                continue

            # Empty line -> possible paragraph break or final break
            if not line:
                if buffer:
                    result.append(self._process_paragraph(" ".join(buffer)))
                    buffer = []
                empty_count += 1
                if empty_count >= 3:
                    result.append({"type": "break"})
                    empty_count = 0
                i += 1
                continue
            else:
                empty_count = 0

            # Heading
            if self.HEADING_PATTERN.match(line):
                if buffer:
                    result.append(self._process_paragraph(" ".join(buffer)))
                    buffer = []
                result.append(self._process_heading(line))
                i += 1
                continue

            # Lists
            if self.LIST_ITEM_PATTERN.match(line):
                if buffer:
                    result.append(self._process_paragraph(" ".join(buffer)))
                    buffer = []
                i = self._process_list(lines, i, result)
                continue

            # Images
            if line.startswith("!["):
                if buffer:
                    result.append(self._process_paragraph(" ".join(buffer)))
                    buffer = []
                image_obj, i = self._process_image(line, lines, i)
                result.append(image_obj)
                continue

            # Tables
            if line.startswith("|"):
                if buffer:
                    result.append(self._process_paragraph(" ".join(buffer)))
                    buffer = []
                i = self._process_table(lines, i, result)
                continue

            # Otherwise treat as normal paragraph text
            buffer.append(line)
            i += 1

        # Any leftover text becomes a paragraph
        if buffer:
            result.append(self._process_paragraph(" ".join(buffer)))

        return result

    def _process_heading(self, line: str) -> Dict:
        m = self.HEADING_PATTERN.match(line)
        if not m:
            return {}
        hashes, text = m.groups()
        level = min(len(hashes), 5)

        ref = None
        # If heading ends with [ref:something], remove that and store
        ref_m = self.REF_PATTERN.search(text)
        if ref_m:
            ref = ref_m.group("ref").strip()
            # strip out the [ref:xxx ...]
            text = self.REF_PATTERN.sub("", text).strip()

        heading_obj = {
            "type": "heading",
            "text": text,
            "level": level,
            "numbered": self.numbered
        }
        if ref:
            heading_obj["ref"] = ref
        return heading_obj

    def _process_list(self, lines: List[str], start_idx: int, result: List) -> int:
        items = []
        i = start_idx
        first_line = lines[i].strip()
        # Determine bullet vs number
        is_numbered = bool(first_line and first_line[0].isdigit())

        while i < len(lines):
            line = lines[i].strip()
            if not line:
                break
            m = self.LIST_ITEM_PATTERN.match(line)
            if m:
                if is_numbered and m.group(1):
                    text = line[line.find('.') + 1:].strip()
                elif not is_numbered and m.group(2):
                    text = line[2:].strip()
                else:
                    break
                tokens = self._process_inline_math_and_formatting(text)
                items.append(tokens if isinstance(tokens, list) else [tokens])
                i += 1
            else:
                break

        result.append({
            "type": "list",
            "style": "number" if is_numbered else "bullet",
            "items": items
        })
        return i

    def _process_image(self, line: str, lines: List[str], idx: int) -> Tuple[Dict, int]:
        alt_m = re.search(r'!\[(.*?)\]', line)
        url_m = re.search(r'\((.*?)\)', line)
        image_obj = {"type": "image"}
        if not alt_m or not url_m:
            return image_obj, idx + 1

        alt_text = alt_m.group(1).strip()
        url_title = url_m.group(1).strip()

        title_m = re.search(r'^(.*?)\s+"(.*?)"$', url_title)
        if title_m:
            image_url = title_m.group(1).strip()
            title_str = title_m.group(2).strip()
        else:
            image_url = url_title
            title_str = None

        image_obj["url"] = self._handle_image_url(image_url)
        if alt_text:
            image_obj["caption"] = alt_text

        if title_str:
            # parse comma-delimited attributes: e.g. caption=..., ref=..., width=...
            for attr in [a.strip() for a in title_str.split(',')]:
                if '=' in attr:
                    k, v = [s.strip() for s in attr.split('=', 1)]
                    if k == 'caption':
                        image_obj["caption"] = v
                    elif k == 'ref':
                        image_obj["ref"] = v
                    elif k == 'width':
                        image_obj["width"] = v
                elif attr == "fullWidth":
                    image_obj["fullWidth"] = True

        return image_obj, idx + 1

    def _handle_image_url(self, url: str) -> str:
        if url.startswith("http") or url.startswith("data:image/"):
            return url

        local = unquote(url)
        if os.path.exists(local) and os.path.isfile(local):
            ext = os.path.splitext(local.lower())[1]
            mime_types = {
                ".png": "image/png",
                ".jpg": "image/jpeg",
                ".jpeg": "image/jpeg",
                ".gif": "image/gif",
                ".bmp": "image/bmp",
                ".webp": "image/webp"
            }
            mime = mime_types.get(ext, "image/png")

            with open(local, "rb") as f:
                data = f.read()
            b64 = base64.b64encode(data).decode("utf-8")
            return f"data:{mime};base64,{b64}"

        raise FileNotFoundError(f"Image file '{local}' not found")

    def _maybe_listify(self, item: Union[str, Dict, List]) -> Union[str, Dict, List]:
        if isinstance(item, list):
            if len(item) == 1:
                return item[0]
            return item
        return item

    def _process_table(self, lines: List[str], start_idx: int, result: List) -> int:
        caption, i = self._find_caption(lines, start_idx, ["Table", "Tab", "TABLE", "TAB"])
        if i >= len(lines) or not lines[i].strip().startswith("|"):
            return i

        # header line
        header_line = lines[i].strip()
        header_cells = [c.strip() for c in header_line.split("|")[1:-1]]
        i += 1

        # skip separator line if present (e.g. |---|---|)
        if i < len(lines) and re.match(r'^\|(?:\s*[-:]+\s*\|)+', lines[i].strip()):
            i += 1

        # table body
        body_raw = []
        while i < len(lines):
            line = lines[i].strip()
            if not line.startswith("|"):
                break
            cells = [cell.strip() for cell in line.split("|")[1:-1]]
            body_raw.append(cells)
            i += 1

        # trailing caption if not found previously
        if not caption:
            caption, i = self._find_caption(lines, i, ["Table", "Tab", "TABLE", "TAB"])

        # convert all cells
        header_processed = [
            self._maybe_listify(self._process_inline_math_and_formatting(h))
            for h in header_cells
        ]
        body_processed = []
        for row in body_raw:
            processed_row = []
            for cell in row:
                cell_content = self._process_inline_math_and_formatting(cell)
                processed_row.append(self._maybe_listify(cell_content))
            body_processed.append(processed_row)

        table_obj = {
            "type": "table",
            "header": header_processed,
            "body": body_processed,
            "caption": caption or ""
        }
        result.append(table_obj)
        return i

    def _find_caption(self, lines: List[str], start_idx: int, prefixes: List[str]) -> Tuple[Optional[str], int]:
        # check a couple lines above
        for idx in range(max(0, start_idx - 2), start_idx):
            l = lines[idx].strip()
            for p in prefixes:
                if re.match(fr'^{p}\.?\s*\d+', l, re.IGNORECASE):
                    return self._clean_caption(l), start_idx
        # check a couple lines below
        for idx in range(start_idx + 1, min(len(lines), start_idx + 3)):
            l = lines[idx].strip()
            for p in prefixes:
                if re.match(fr'^{p}\.?\s*\d+', l, re.IGNORECASE):
                    return self._clean_caption(l), idx + 1
        return None, start_idx

    def _clean_caption(self, text: str) -> str:
        m = re.match(
            r'^(?:Table|Tab|TABLE|TAB|Figure|Fig|FIGURE|FIG)\.?\s*\d+(?:\.\d+)*\s*[-:~]?\s*(.*)',
            text,
            re.IGNORECASE
        )
        return m.group(1).strip() if m else text.strip()

    def _process_footnotes(self, text: str) -> Tuple[str, Dict[str, str]]:
        footnotes = {}

        def repl(m):
            footnotes[m.group(1)] = m.group(2).strip()
            return ""

        text = self.FOOTNOTE_DEF_PATTERN.sub(repl, text)
        text = self.FOOTNOTE_REF_PATTERN.sub(lambda m: f"__FOOTNOTE__{m.group(1)}__", text)
        return text, footnotes

    def _process_paragraph(self, text: str) -> Dict:
        if not text:
            return {"type": "paragraph", "text": []}

        parts = text.split("__FOOTNOTE__")
        content = []
        for part in parts:
            if "__" in part:
                # part looks like "12__ some text here"
                fid, rem = part.split("__", 1)
                content.append({"type": "footnote", "text": self.footnotes.get(fid, "")})
                if rem:
                    tokens = self._process_inline_math_and_formatting(rem.strip())
                    if isinstance(tokens, list):
                        content.extend(tokens)
                    elif tokens:
                        content.append(tokens)
            else:
                tokens = self._process_inline_math_and_formatting(part.strip())
                if isinstance(tokens, list):
                    content.extend(tokens)
                elif tokens:
                    content.append(tokens)

        return {"type": "paragraph", "text": content if content else [""]}

    def _process_inline_math_and_formatting(self, text: str) -> Union[str, List]:
        """
        Finds inline math ($...$), splits them out, and processes
        each non‐math segment for additional formatting.
        """
        segments = []
        last = 0
        for m in self.INLINE_MATH_PATTERN.finditer(text):
            if m.start() > last:
                segments.append(self._process_inline_formatting(text[last:m.start()]))
            # This is an equation
            segments.append({"type": "equation", "equation": m.group(1).strip()})
            last = m.end()
        if last < len(text):
            segments.append(self._process_inline_formatting(text[last:]))

        # Flatten
        flat = []
        for seg in segments:
            if isinstance(seg, list):
                flat.extend(seg)
            elif seg:
                flat.append(seg)

        if not flat:
            return ""
        if len(flat) == 1:
            return flat[0]
        return flat

    def _process_inline_formatting(self, text: str) -> Union[str, List]:
        """
        Recursively processes all inline formatting
        (bold, italic, underline, etc.), as well as
        [ref: ...] patterns for references or crossReferences.
        """
        tokens = []
        pos = 0
        while pos < len(text):
            # 1) Check for inline math at current position
            math_match = self.INLINE_MATH_PATTERN.match(text, pos)
            if math_match:
                tokens.append({"type": "equation", "equation": math_match.group(1).strip()})
                pos = math_match.end()
                continue

            # 2) Check for [ref: ...] at current position
            ref_match = self.REF_PATTERN.match(text, pos)
            if ref_match:
                ref_id = ref_match.group("ref")
                label = ref_match.group("label")
                if label:
                    # Cross reference
                    tokens.append({
                        "type": "crossReference",
                        "ref": ref_id,
                        "label": label
                    })
                else:
                    # In-line reference to a bibliography entry
                    tokens.append({
                        "type": "reference",
                        "ref": ref_id
                    })
                pos = ref_match.end()
                continue

            # 3) Try each of the other formatting patterns
            match_found = False
            for fmt, pattern in self.INLINE_FORMATTING_PATTERNS.items():
                m = pattern.match(text, pos)
                if m:
                    inner_text = m.group(1)
                    inner_tokens = self._process_inline_formatting(inner_text)
                    flag = {}
                    if fmt == "bold_italic":
                        flag["bold"] = True
                        flag["italic"] = True
                    elif fmt == "bold":
                        flag["bold"] = True
                    elif fmt == "italic":
                        flag["italic"] = True
                    elif fmt == "underline":
                        flag["underline"] = True
                    elif fmt in ["superscript_md", "superscript_html"]:
                        flag["superscript"] = True
                    elif fmt in ["subscript_md", "subscript_html"]:
                        flag["subscript"] = True
                    elif fmt == "hyperlink":
                        # group(1) is link text, group(2) is url
                        # We'll store as FormattedText with a url
                        link_text = inner_text
                        link_url = m.group(2)
                        tokens.append({
                            "text": link_text,
                            "url": link_url
                        })
                        pos = m.end()
                        match_found = True
                        break

                    # If not a hyperlink, we merge the flags with the inner tokens
                    if fmt != "hyperlink":
                        if isinstance(inner_tokens, list):
                            for token in inner_tokens:
                                if isinstance(token, dict):
                                    merged = dict(flag)
                                    merged.update(token)
                                    tokens.append(merged)
                                else:
                                    tokens.append({**flag, "text": token})
                        else:
                            if isinstance(inner_tokens, dict):
                                merged = dict(flag)
                                merged.update(inner_tokens)
                                tokens.append(merged)
                            else:
                                tokens.append({**flag, "text": inner_tokens})

                        pos = m.end()
                        match_found = True
                        break

            if match_found:
                continue

            # 4) If no special match, grab plain text up to the next pattern
            next_pos = len(text)
            # Gather next boundary among math, ref, or any pattern in INLINE_FORMATTING_PATTERNS
            for pat in [self.INLINE_MATH_PATTERN, self.REF_PATTERN] + list(self.INLINE_FORMATTING_PATTERNS.values()):
                nm = pat.search(text, pos)
                if nm:
                    next_pos = min(next_pos, nm.start())
            tokens.append(text[pos:next_pos])
            pos = next_pos

        # Remove empty strings
        tokens = [t for t in tokens if t != ""]
        if len(tokens) == 1:
            return tokens[0]
        return tokens
