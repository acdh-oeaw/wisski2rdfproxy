from pydantic import BaseModel, AnyUrl
from rdfproxy import SPARQLBinding

class ExternalAuthority(BaseModel):
    class Config:
        title = "External Authority"
    external_authority_display_name: Annotated[str, SPARQLBinding("?external_authority__external_authority_display_name")]
    external_authority_url: Annotated[AnyUrl, SPARQLBinding("?external_authority__external_authority_url")]


class Person(BaseModel):
    class Config:
        title = "Person"
    person_id_assignment: list[Annotated[None, SPARQLBinding("?person__person_id_assignment")]]
    person_gender_assertion: list[Annotated[AnyUrl, SPARQLBinding("?person__person_gender_assertion")]]
    person_ethnicity_assertion: list[Annotated[AnyUrl, SPARQLBinding("?person__person_ethnicity_assertion")]]
    person_descriptive_name: list[Annotated[str, SPARQLBinding("?person__person_descriptive_name")]]
    person_possession_assertion: list[Annotated[AnyUrl, SPARQLBinding("?person__person_possession_assertion")]]
    person_status_assertion: list[Annotated[AnyUrl, SPARQLBinding("?person__person_status_assertion")]]
    person_religion_assertion: list[Annotated[AnyUrl, SPARQLBinding("?person__person_religion_assertion")]]
    person_occupation_assertion: list[Annotated[AnyUrl, SPARQLBinding("?person__person_occupation_assertion")]]
    person_language_assertion: list[Annotated[AnyUrl, SPARQLBinding("?person__person_language_assertion")]]
    person_kinship_assertion: list[Annotated[AnyUrl, SPARQLBinding("?person__person_kinship_assertion")]]
    birth_circumstances_claim: Annotated[AnyUrl, SPARQLBinding("?person__birth_circumstances_claim")]
    person_death_assertion: Annotated[AnyUrl, SPARQLBinding("?person__person_death_assertion")]


class PersonPersonIdAssignment(BaseModel):
    class Config:
        title = "Identity in other services"
    external_authority: list[Annotated[None, SPARQLBinding("?person__person_id_assignment__person_identifier_by__external_authority")]]
    person_identifier: Annotated[None, SPARQLBinding("?person__person_id_assignment__person_identifier")]


class PersonPersonIdAssignmentPersonIdentifier(BaseModel):
    class Config:
        title = "External identifier"
    person_identifier_is: Annotated[AnyUrl, SPARQLBinding("?person__person_id_assignment__person_identifier__person_identifier_is")]
    person_identifier_plain: Annotated[str, SPARQLBinding("?person__person_id_assignment__person_identifier__person_identifier_plain")]


class PersonPersonIdAssignmentPersonIdentifierByExternalAuthority(BaseModel):
    class Config:
        title = "External Authority"
    external_authority_display_name: Annotated[str, SPARQLBinding("?person__person_id_assignment__person_identifier_by__external_authority__external_authority_display_name")]
    external_authority_url: Annotated[AnyUrl, SPARQLBinding("?person__person_id_assignment__person_identifier_by__external_authority__external_authority_url")]


class Publication(BaseModel):
    class Config:
        title = "Publication"
    publication_reference: Annotated[str, SPARQLBinding("?publication__publication_reference")]
    publication_creation: list[Annotated[None, SPARQLBinding("?publication__publication_creation")]]


class PublicationPublicationCreation(BaseModel):
    class Config:
        title = "Publication creation"
    publication_creation_event: Annotated[AnyUrl, SPARQLBinding("?publication__publication_creation__publication_creation_event")]


