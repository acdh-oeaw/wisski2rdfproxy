from pydantic import BaseModel, AnyUrl
from rdfproxy import SPARQLBinding

class ExternalAuthority(BaseModel):
    class Config:
        title = "External Authority"
        original_path_id = "external_authority"
    external_authority_display_name: Annotated[str, SPARQLBinding("external_authority__external_authority_display_name")]
    external_authority_url: Annotated[AnyUrl, SPARQLBinding("external_authority__external_authority_url")]


