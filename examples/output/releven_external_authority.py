from typing import Annotated

from pydantic import AnyUrl, BaseModel
from rdfproxy import SPARQLBinding


class ExternalAuthority(BaseModel):
    class Config:
        title = "External Authority"
        model_bool = "id"
    id: Annotated[AnyUrl | None, SPARQLBinding("external_authority")] = None
    external_authority_display_name: Annotated[str, SPARQLBinding(
        "external_authority__external_authority_display_name")]
    external_authority_url: Annotated[AnyUrl, SPARQLBinding(
        "external_authority__external_authority_url")]

