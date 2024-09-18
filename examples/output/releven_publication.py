from pydantic import BaseModel, AnyUrl
from rdfproxy import SPARQLBinding
from typing import Annotated

class Publication_PublicationCreation(BaseModel):
    class Config:
        title = "Publication creation"
        original_path_id = "publication_creation"
    publication_creation_event: Annotated[AnyUrl, SPARQLBinding("publication__publication_creation__publication_creation_event")]


class Publication(BaseModel):
    class Config:
        title = "Publication"
        original_path_id = "publication"
    publication_reference: Annotated[str, SPARQLBinding("publication__publication_reference")]
    publication_creation: list[Publication_PublicationCreation]


