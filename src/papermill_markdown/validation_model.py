# src/validation_model.py

from pydantic import BaseModel, Field
from typing import List, Optional, Union, Literal, ClassVar

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

# Union type for text content
TextContent = Union[str, FormattedText, CrossReference, Footnote, Code, Equation]

# Document content models
class Heading(BaseModel):
    type: Literal["heading"]
    text: str
    level: int = Field(ge=1, le=5)
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
    header: List[str]
    body: List[List[str]]
    caption: Optional[str] = None
    transpose: Optional[bool] = None

class DocumentList(BaseModel):
    type: Literal["list"]
    style: Literal["bullet", "number"]
    items: List[Union[str, List[TextContent]]]

# Include Break in the union for document elements.
DocumentElement = Union[Heading, Paragraph, Image, Table, DocumentList, Equation, Code, Break]

class DocumentContent(BaseModel):
    documentContent: ClassVar[List[DocumentElement]]

class PapermillDocument(DocumentContent):
    layoutId: str

    class Config:
        extra = "allow"

