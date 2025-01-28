from pydantic import AnyUrl, BaseModel, Field  # noqa: F401
from rdfproxy import ConfigDict, SPARQLBinding
from typing import Annotated


class ExternalAuthority(BaseModel):
    model_config = ConfigDict(
        title="External Authority",
        model_bool="id",
    )
    id: Annotated[AnyUrl | None, SPARQLBinding("External_authority")] = Field(
        default=None, exclude=False
    )
    external_authority_display_name: Annotated[
        str, SPARQLBinding("External_authority__external_authority_display_name")
    ]
    external_authority_url: Annotated[
        AnyUrl, SPARQLBinding("External_authority__external_authority_url")
    ]
