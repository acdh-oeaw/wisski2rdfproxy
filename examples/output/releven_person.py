from pydantic import BaseModel, AnyUrl
from rdfproxy import SPARQLBinding
from typing import Annotated

class Person_PersonAppellationAssertion_PersonAppellationSource(BaseModel):
    class Config:
        title = "Source"
        original_path_id = "source"
        group_by = "person__person_appellation_assertion__person_appellation_source"
    source_publication: Annotated[AnyUrl, SPARQLBinding("person__person_appellation_assertion__person_appellation_source__source_publication")]
    source_seal: Annotated[AnyUrl, SPARQLBinding("person__person_appellation_assertion__person_appellation_source__source_seal")]
    source_reference: Annotated[str, SPARQLBinding("person__person_appellation_assertion__person_appellation_source__source_reference")]
    source_content: Annotated[str, SPARQLBinding("person__person_appellation_assertion__person_appellation_source__source_content")]


class Person_PersonAppellationAssertion(BaseModel):
    class Config:
        title = "Name(s) in the sources"
        original_path_id = "person_appellation_assertion"
        group_by = "person__person_appellation_assertion"
    person_appellation_source: Annotated[Person_PersonAppellationAssertion_PersonAppellationSource, SPARQLBinding("person__person_appellation_assertion__person_appellation_source")]
    person_appellation_is: Annotated[str, SPARQLBinding("person__person_appellation_assertion__person_appellation_is")]


class Person(BaseModel):
    class Config:
        title = "Person"
        original_path_id = "person"
        group_by = "person"
    person_id_assignment: Annotated[list[AnyUrl], SPARQLBinding("person__person_id_assignment")]
    person_appellation_assertion: Annotated[list[Person_PersonAppellationAssertion], SPARQLBinding("person__person_appellation_assertion")]
    person_gender_assertion: Annotated[list[AnyUrl], SPARQLBinding("person__person_gender_assertion")]
    person_ethnicity_assertion: Annotated[list[AnyUrl], SPARQLBinding("person__person_ethnicity_assertion")]
    person_descriptive_name: Annotated[list[str], SPARQLBinding("person__person_descriptive_name")]
    person_possession_assertion: Annotated[list[AnyUrl], SPARQLBinding("person__person_possession_assertion")]
    person_status_assertion: Annotated[list[AnyUrl], SPARQLBinding("person__person_status_assertion")]
    person_religion_assertion: Annotated[list[AnyUrl], SPARQLBinding("person__person_religion_assertion")]
    person_occupation_assertion: Annotated[list[AnyUrl], SPARQLBinding("person__person_occupation_assertion")]
    person_language_assertion: Annotated[list[AnyUrl], SPARQLBinding("person__person_language_assertion")]
    person_kinship_assertion: Annotated[list[AnyUrl], SPARQLBinding("person__person_kinship_assertion")]
    birth_circumstances_claim: Annotated[AnyUrl, SPARQLBinding("person__birth_circumstances_claim")]
    person_death_assertion: Annotated[AnyUrl, SPARQLBinding("person__person_death_assertion")]


