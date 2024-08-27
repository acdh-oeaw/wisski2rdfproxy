from pydantic import BaseModel, AnyUrl
from rdfproxy import SPARQLBinding

class Person(BaseModel):
    class Config:
        title = "Person"
    person_id_assignment: list[Annotated[None, SPARQLBinding("?person_person_id_assignment")]]
    person_ethnicity_assertion: list[Annotated[AnyUrl, SPARQLBinding("?person_person_ethnicity_assertion")]]
    person_descriptive_name: list[Annotated[str, SPARQLBinding("?person_person_descriptive_name")]]
    person_possession_assertion: list[Annotated[AnyUrl, SPARQLBinding("?person_person_possession_assertion")]]
    person_status_assertion: list[Annotated[AnyUrl, SPARQLBinding("?person_person_status_assertion")]]
    person_religion_assertion: list[Annotated[AnyUrl, SPARQLBinding("?person_person_religion_assertion")]]
    person_occupation_assertion: list[Annotated[AnyUrl, SPARQLBinding("?person_person_occupation_assertion")]]
    person_language_assertion: list[Annotated[AnyUrl, SPARQLBinding("?person_person_language_assertion")]]
    person_kinship_assertion: list[Annotated[AnyUrl, SPARQLBinding("?person_person_kinship_assertion")]]
    birth_circumstances_claim: Annotated[AnyUrl, SPARQLBinding("?person_birth_circumstances_claim")]
    person_death_assertion: Annotated[AnyUrl, SPARQLBinding("?person_person_death_assertion")]


class PersonPersonIdAssignment(BaseModel):
    class Config:
        title = "Identity in other services"
    external_authority: list[Annotated[None, SPARQLBinding("?person_person_id_assignment_person_identifier_by_external_authority")]]
    person_identifier: Annotated[None, SPARQLBinding("?person_person_id_assignment_person_identifier")]


class PersonPersonIdAssignmentPersonIdentifier(BaseModel):
    class Config:
        title = "External identifier"
    person_identifier_is: Annotated[AnyUrl, SPARQLBinding("?person_person_id_assignment_person_identifier_person_identifier_is")]
    person_identifier_plain: Annotated[str, SPARQLBinding("?person_person_id_assignment_person_identifier_person_identifier_plain")]


class PersonPersonIdAssignmentPersonIdentifierByExternalAuthority(BaseModel):
    class Config:
        title = "External Authority"
    external_authority_display_name: Annotated[str, SPARQLBinding("?person_person_id_assignment_person_identifier_by_external_authority_external_authority_display_name")]
    external_authority_url: Annotated[AnyUrl, SPARQLBinding("?person_person_id_assignment_person_identifier_by_external_authority_external_authority_url")]


