from typing import Annotated

from pydantic import AnyUrl, BaseModel
from rdfproxy import SPARQLBinding


class ExternalAuthority(BaseModel):
    class Config:
        title = "External Authority"
        model_bool = "external_authority"
    external_authority_display_name: Annotated[str | None, SPARQLBinding(
        "external_authority__external_authority_display_name")]
    external_authority_url: Annotated[AnyUrl | None, SPARQLBinding(
        "external_authority__external_authority_url")]

