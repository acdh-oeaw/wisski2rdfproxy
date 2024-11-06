from pydantic import BaseModel, AnyUrl
from rdfproxy import SPARQLBinding
from typing import Annotated

class Publication_PublicationCreation(BaseModel):
    class Config:
        title = "Publication creation"
        model_bool = "publication__publication_creation"
    publication_creation_event: Annotated[AnyUrl, SPARQLBinding("publication__publication_creation__publication_creation_event")]


class Publication(BaseModel):
    class Config:
        title = "Publication"
        model_bool = "publication"
        group_by = "publication"
    publication_reference: Annotated[str, SPARQLBinding("publication__publication_reference")]
    publication_creation: Annotated[list[Publication_PublicationCreation], SPARQLBinding("publication__publication_creation")]


