from typing import Annotated

from pydantic import AnyUrl, BaseModel, Field  # noqa: F401
from rdfproxy import ConfigDict, SPARQLBinding


class ExternalAuthority(BaseModel):
    model_config = ConfigDict(title="External Authority",
                              model_bool="id",)
    id: Annotated[AnyUrl | None, SPARQLBinding(
        "external_authority")] = Field(default=None, exclude=True)
    external_authority_display_name: Annotated[str, SPARQLBinding(
        "external_authority__external_authority_display_name")]
    external_authority_url: Annotated[AnyUrl, SPARQLBinding(
        "external_authority__external_authority_url")]

