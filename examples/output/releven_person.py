from pydantic import BaseModel, AnyUrl
from rdfproxy import SPARQLBinding

class Person(BaseModel):
    class Config:
        title = "Person"
        original_path_id = "person"
    person_id_assignment: list[Annotated[AnyUrl, SPARQLBinding("person__person_id_assignment")]]
    person_appellation_assertion: list[Person_PersonAppellationAssertion]
    person_gender_assertion: list[Annotated[AnyUrl, SPARQLBinding("person__person_gender_assertion")]]
    person_ethnicity_assertion: list[Annotated[AnyUrl, SPARQLBinding("person__person_ethnicity_assertion")]]
    person_descriptive_name: list[Annotated[str, SPARQLBinding("person__person_descriptive_name")]]
    person_possession_assertion: list[Annotated[AnyUrl, SPARQLBinding("person__person_possession_assertion")]]
    person_status_assertion: list[Annotated[AnyUrl, SPARQLBinding("person__person_status_assertion")]]
    person_religion_assertion: list[Annotated[AnyUrl, SPARQLBinding("person__person_religion_assertion")]]
    person_occupation_assertion: list[Annotated[AnyUrl, SPARQLBinding("person__person_occupation_assertion")]]
    person_language_assertion: list[Annotated[AnyUrl, SPARQLBinding("person__person_language_assertion")]]
    person_kinship_assertion: list[Annotated[AnyUrl, SPARQLBinding("person__person_kinship_assertion")]]
    birth_circumstances_claim: Annotated[AnyUrl, SPARQLBinding("person__birth_circumstances_claim")]
    person_death_assertion: Annotated[AnyUrl, SPARQLBinding("person__person_death_assertion")]


class Person_PersonAppellationAssertion(BaseModel):
    class Config:
        title = "Name(s) in the sources"
        original_path_id = "person_appellation_assertion"
    person_appellation_source: Person_PersonAppellationAssertion_PersonAppellationSource
    person_appellation_is: Annotated[str, SPARQLBinding("person__person_appellation_assertion__person_appellation_is")]


class Person_PersonAppellationAssertion_PersonAppellationSource(BaseModel):
    class Config:
        title = "Source"
        original_path_id = "source"
    source_publication: Annotated[AnyUrl, SPARQLBinding("person__person_appellation_assertion__person_appellation_source__source_publication")]
    source_seal: Annotated[AnyUrl, SPARQLBinding("person__person_appellation_assertion__person_appellation_source__source_seal")]
    source_reference: Annotated[str, SPARQLBinding("person__person_appellation_assertion__person_appellation_source__source_reference")]
    source_content: Annotated[str, SPARQLBinding("person__person_appellation_assertion__person_appellation_source__source_content")]


