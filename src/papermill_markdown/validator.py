# src/papermill_markdown/validator.py

from pydantic import RootModel, BaseModel, Field, model_validator
from typing import List, Union, Literal, Optional, Dict

# ==================
# 1) Add a new ReferenceObject and top-level references property
# ==================
class ReferenceObject(BaseModel):
    bibtex: Optional[str] = None
    isbn: Optional[str] = None
    doi: Optional[str] = None

    @model_validator(mode="after")
    def check_at_least_one(self) -> "ReferenceObject":
        if not (self.bibtex or self.isbn or self.doi):
            raise ValueError("A reference must have at least one of: bibtex, isbn, doi.")
        return self



# ==================
# Inline content models
# ==================
class FormattedText(BaseModel):
    text: str
    bold: Optional[bool] = None
    italic: Optional[bool] = None
    underline: Optional[bool] = None
    superscript: Optional[bool] = None
    subscript: Optional[bool] = None
    url: Optional[str] = None

class CrossReference(BaseModel):
    type: Literal["crossReference"]
    ref: str
    label: str = "section"

class Footnote(BaseModel):
    type: Literal["footnote"]
    text: str

class Code(BaseModel):
    type: Literal["code"]
    text: str

class Equation(BaseModel):
    type: Literal["equation"]
    equation: str

class Break(BaseModel):
    type: Literal["break"]

# ==================
# 2) Add a new ReferenceInline for in-line references
# ==================
class ReferenceInline(BaseModel):
    type: Literal["reference"]
    ref: str

# Union for inline text content
TextContent = Union[str, FormattedText, CrossReference, Footnote, Code, Equation, ReferenceInline]

# A cell in the table can be:
# - a simple string,
# - a single inline element (Equation, Footnote, FormattedText, etc.),
# - or a list of inline elements
CellContent = Union[str, TextContent, List[TextContent]]

# Block element models
class Heading(BaseModel):
    type: Literal["heading"]
    text: str
    level: int = Field(..., ge=1, le=5)
    ref: Optional[str] = None
    numbered: Optional[bool] = None

class Paragraph(BaseModel):
    type: Literal["paragraph"]
    text: Union[str, List[TextContent]]
    style: Optional[str] = None  # e.g. "preview"

class Image(BaseModel):
    type: Literal["image"]
    url: str
    caption: Optional[Union[str, List[Union[str, FormattedText]]]] = None
    width: Optional[str] = None
    ref: Optional[str] = None

class Table(BaseModel):
    type: Literal["table"]
    header: List[CellContent]
    body: List[List[CellContent]]
    caption: Optional[Union[str, List[TextContent]]] = None
    transpose: Optional[bool] = None

class DocumentList(BaseModel):
    type: Literal["list"]
    style: Literal["bullet", "number"]
    items: List[Union[str, List[TextContent]]]

# Union of all document elements
DocumentElement = Union[
    Heading,
    Paragraph,
    Image,
    Table,
    DocumentList,
    Equation,
    Code,
    Break
]

# ==================
# 3) For code compatibility, keep DocumentContent as is,
#    but typically you'd have a new top-level "DocumentModel"
#    that includes references + content. Example:
# ==================
class DocumentContent(RootModel[List[DocumentElement]]):
    def get_elements(self) -> List[DocumentElement]:
        return self.__root__


# NEW/UPDATED: an optional top-level model if desired:
class DocumentModel(BaseModel):
    # “references” can be included at the top level
    references: Optional[Dict[str, ReferenceObject]] = None
    # The main content
    documentContent: DocumentContent
