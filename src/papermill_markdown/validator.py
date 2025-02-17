# src/papermill_markdown/validator.py

from pydantic import RootModel
from typing import List, Union, Literal, Optional
from pydantic import BaseModel, Field

# Inline content models
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

# Union for inline text content
TextContent = Union[str, FormattedText, CrossReference, Footnote, Code, Equation]

# A cell in the table can be:
#  - a simple string,
#  - a single inline element (Equation, Footnote, FormattedText, etc.),
#  - or a list of inline elements (mixed text + equation, etc.)
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

class Image(BaseModel):
    type: Literal["image"]
    url: str
    caption: Optional[Union[str, List[Union[str, FormattedText]]]] = None
    width: Optional[str] = None
    ref: Optional[str] = None

class Table(BaseModel):
    type: Literal["table"]
    # Now allow each header cell to be any valid "CellContent"
    header: List[CellContent]
    # Each row is a list of "CellContent"
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

# Validator for an entire document (a list of DocumentElement)
class DocumentContent(RootModel[List[DocumentElement]]):
    def get_elements(self) -> List[DocumentElement]:
        return self.__root__
