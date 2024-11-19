from typing import Annotated

from pydantic import AnyUrl, BaseModel
from rdfproxy import SPARQLBinding


class Boulloterion_BoulloterionSealAssertion_BoulloterionSealBy6606A275376D5(BaseModel):
    class Config:
        title = "Author list"
        model_bool = "boulloterion__boulloterion_seal_assertion__boulloterion_seal_by_6606a275376d5"
        group_by = "boulloterion__boulloterion_seal_assertion__boulloterion_seal_by_6606a275376d5"
    author_list_members: Annotated[list[AnyUrl], SPARQLBinding(
        "boulloterion__boulloterion_seal_assertion__boulloterion_seal_by_6606a275376d5__author_list_members")]
    author_list_namestring: Annotated[str | None, SPARQLBinding(
        "boulloterion__boulloterion_seal_assertion__boulloterion_seal_by_6606a275376d5__author_list_namestring")]


class Boulloterion_BoulloterionSealAssertion(BaseModel):
    class Config:
        title = "boulloterion_seal_assertion"
        model_bool = "boulloterion__boulloterion_seal_assertion"
    boulloterion_seal_by: Annotated[AnyUrl | None, SPARQLBinding(
        "boulloterion__boulloterion_seal_assertion__boulloterion_seal_by")]
    boulloterion_produced_seal: Annotated[None | None, SPARQLBinding(
        "boulloterion__boulloterion_seal_assertion__boulloterion_produced_seal")]
    boulloterion_seal_by_6606a275376d5: Annotated[Boulloterion_BoulloterionSealAssertion_BoulloterionSealBy6606A275376D5 | None, SPARQLBinding(
        "boulloterion__boulloterion_seal_assertion__boulloterion_seal_by_6606a275376d5")]
    boulloterion_seal_source: Annotated[AnyUrl | None, SPARQLBinding(
        "boulloterion__boulloterion_seal_assertion__boulloterion_seal_source")]


class Boulloterion(BaseModel):
    class Config:
        title = "Boulloterion"
        model_bool = "boulloterion"
        group_by = "boulloterion"
    boulloterion_seal_assertion: Annotated[list[Boulloterion_BoulloterionSealAssertion], SPARQLBinding(
        "boulloterion__boulloterion_seal_assertion")]
    boulloterion_description: Annotated[str | None, SPARQLBinding(
        "boulloterion__boulloterion_description")]

