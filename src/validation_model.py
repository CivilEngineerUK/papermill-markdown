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

class Math(BaseModel):
    type: Literal["math"]
    text: str

# Union type for text content
TextContent = Union[str, FormattedText, CrossReference, Footnote, Code, Math]

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
    caption: Optional[str] = None
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

class Placeholders(BaseModel):
    RecipientName: Optional[str] = None
    RecipientJobTitle: Optional[str] = None
    CompanyName: Optional[str] = None
    CompanyAddress: Optional[str] = None
    CompanyAddress2: Optional[str] = None
    CompanyCity: Optional[str] = None
    CompanyPostcode: Optional[str] = None
    Date: Optional[str] = None
    AuthorName: Optional[str] = None
    AuthorJobTitle: Optional[str] = None

class DocumentContent(BaseModel):
    documentContent: ClassVar[List[Union[Heading, Paragraph, Image, Table, DocumentList, Math]]]

class PapermillDocument(DocumentContent):
    layoutId: str
    placeholders: Placeholders