from pydantic import BaseModel, AnyUrl
from rdfproxy import SPARQLBinding
from typing import Annotated

class ExternalAuthority(BaseModel):
    class Config:
        title = "External Authority"
        model_bool = "external_authority"
    external_authority_display_name: Annotated[str, SPARQLBinding("external_authority__external_authority_display_name")]
    external_authority_url: Annotated[AnyUrl, SPARQLBinding("external_authority__external_authority_url")]


