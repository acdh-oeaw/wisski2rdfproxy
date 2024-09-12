from pydantic import BaseModel, AnyUrl
from rdfproxy import SPARQLBinding

class ExternalAuthority(BaseModel):
    class Config:
        title = "External Authority"
        original_path_id = "external_authority"
    external_authority_display_name: Annotated[str, SPARQLBinding("?external_authority__external_authority_display_name")]
    external_authority_url: Annotated[AnyUrl, SPARQLBinding("?external_authority__external_authority_url")]


class Publication(BaseModel):
    class Config:
        title = "Publication"
        original_path_id = "publication"
    publication_reference: Annotated[str, SPARQLBinding("?publication__publication_reference")]
    publication_creation: list[Publication_PublicationCreation]


class Publication_PublicationCreation(BaseModel):
    class Config:
        title = "Publication creation"
        original_path_id = "publication_creation"
    publication_creation_event: Annotated[AnyUrl, SPARQLBinding("?publication__publication_creation__publication_creation_event")]


