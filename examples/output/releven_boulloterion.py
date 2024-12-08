from typing import Annotated

from pydantic import AnyUrl, BaseModel, Field  # noqa: F401
from rdfproxy import ConfigDict, SPARQLBinding


class Boulloterion_BoulloterionSealAssertion_BoulloterionSealBy6606A275376D5(BaseModel):
    model_config = ConfigDict(title="Author list",
                              model_bool="id",
                              group_by="id",)
    id: Annotated[AnyUrl | None, SPARQLBinding(
        "boulloterion__boulloterion_seal_assertion__boulloterion_seal_by_6606a275376d5")] = Field(default=None, exclude=True)
    author_list_members: Annotated[list[AnyUrl], SPARQLBinding(
        "boulloterion__boulloterion_seal_assertion__boulloterion_seal_by_6606a275376d5__author_list_members")]
    author_list_namestring: Annotated[str, SPARQLBinding(
        "boulloterion__boulloterion_seal_assertion__boulloterion_seal_by_6606a275376d5__author_list_namestring")]


class Boulloterion_BoulloterionSealAssertion(BaseModel):
    model_config = ConfigDict(title="boulloterion_seal_assertion",
                              model_bool="id",)
    id: Annotated[AnyUrl | None, SPARQLBinding(
        "boulloterion__boulloterion_seal_assertion")] = Field(default=None, exclude=True)
    boulloterion_seal_by: Annotated[AnyUrl, SPARQLBinding(
        "boulloterion__boulloterion_seal_assertion__boulloterion_seal_by")]
    boulloterion_produced_seal: Annotated[None, SPARQLBinding(
        "boulloterion__boulloterion_seal_assertion__boulloterion_produced_seal")]
    boulloterion_seal_by_6606a275376d5: Annotated[Boulloterion_BoulloterionSealAssertion_BoulloterionSealBy6606A275376D5, SPARQLBinding(
        "boulloterion__boulloterion_seal_assertion__boulloterion_seal_by_6606a275376d5")]
    boulloterion_seal_source: Annotated[AnyUrl, SPARQLBinding(
        "boulloterion__boulloterion_seal_assertion__boulloterion_seal_source")]


class Boulloterion(BaseModel):
    model_config = ConfigDict(title="Boulloterion",
                              model_bool="id",
                              group_by="id",)
    id: Annotated[AnyUrl | None, SPARQLBinding(
        "boulloterion")] = Field(default=None, exclude=True)
    boulloterion_seal_assertion: Annotated[list[Boulloterion_BoulloterionSealAssertion], SPARQLBinding(
        "boulloterion__boulloterion_seal_assertion")]
    boulloterion_description: Annotated[str, SPARQLBinding(
        "boulloterion__boulloterion_description")]

