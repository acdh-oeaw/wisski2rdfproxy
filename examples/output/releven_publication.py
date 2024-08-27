from pydantic import BaseModel, AnyUrl
from rdfproxy import SPARQLBinding

class Publication(BaseModel):
    class Config:
        title = "Publication"
    publication_reference: Annotated[str, SPARQLBinding("?publication_publication_reference")]
    publication_creation: list[Annotated[None, SPARQLBinding("?publication_publication_creation")]]
    publication_text_assertion: list[Annotated[None, SPARQLBinding("?publication_publication_text_assertion")]]


class PublicationPublicationCreation(BaseModel):
    class Config:
        title = "Publication creation"
    publication_creation_event: Annotated[None, SPARQLBinding("?publication_publication_creation_publication_creation_event")]


