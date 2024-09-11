from pydantic import BaseModel, AnyUrl
from rdfproxy import SPARQLBinding

class ExternalAuthority(BaseModel):
    class Config:
        title = "External Authority"
        original_path_id = "external_authority"
    external_authority_display_name: Annotated[str, SPARQLBinding("?external_authority_display_name")]
    external_authority_url: Annotated[AnyUrl, SPARQLBinding("?external_authority_url")]


class Person(BaseModel):
    class Config:
        title = "Person"
        original_path_id = "person"
    person_id_assignment: list[Annotated[Person_PersonIdAssignment, SPARQLBinding("?person_id_assignment")]]
    person_gender_assertion: list[Annotated[AnyUrl, SPARQLBinding("?person_gender_assertion")]]
    person_ethnicity_assertion: list[Annotated[AnyUrl, SPARQLBinding("?person_ethnicity_assertion")]]
    person_descriptive_name: list[Annotated[str, SPARQLBinding("?person_descriptive_name")]]
    person_possession_assertion: list[Annotated[AnyUrl, SPARQLBinding("?person_possession_assertion")]]
    person_status_assertion: list[Annotated[AnyUrl, SPARQLBinding("?person_status_assertion")]]
    person_religion_assertion: list[Annotated[AnyUrl, SPARQLBinding("?person_religion_assertion")]]
    person_occupation_assertion: list[Annotated[AnyUrl, SPARQLBinding("?person_occupation_assertion")]]
    person_language_assertion: list[Annotated[AnyUrl, SPARQLBinding("?person_language_assertion")]]
    person_kinship_assertion: list[Annotated[AnyUrl, SPARQLBinding("?person_kinship_assertion")]]
    birth_circumstances_claim: Annotated[AnyUrl, SPARQLBinding("?birth_circumstances_claim")]
    person_death_assertion: Annotated[AnyUrl, SPARQLBinding("?person_death_assertion")]


class Person_PersonIdAssignment(BaseModel):
    class Config:
        title = "Identity in other services"
        original_path_id = "person_id_assignment"
    person_identifier_by: Annotated[Person_PersonIdAssignment_PersonIdentifierBy, SPARQLBinding("?person_identifier_by")]
    person_identifier: Annotated[Person_PersonIdAssignment_PersonIdentifier, SPARQLBinding("?person_identifier")]


class Person_PersonIdAssignment_PersonIdentifier(BaseModel):
    class Config:
        title = "External identifier"
        original_path_id = "person_identifier"
    person_identifier_is: Annotated[AnyUrl, SPARQLBinding("?person_identifier_is")]
    person_identifier_plain: Annotated[str, SPARQLBinding("?person_identifier_plain")]


class Person_PersonIdAssignment_PersonIdentifierBy(BaseModel):
    class Config:
        title = "External Authority"
        original_path_id = "external_authority"
    external_authority_display_name: Annotated[str, SPARQLBinding("?external_authority_display_name")]
    external_authority_url: Annotated[AnyUrl, SPARQLBinding("?external_authority_url")]


class Publication(BaseModel):
    class Config:
        title = "Publication"
        original_path_id = "publication"
    publication_reference: Annotated[str, SPARQLBinding("?publication_reference")]
    publication_creation: list[Annotated[Publication_PublicationCreation, SPARQLBinding("?publication_creation")]]


class Publication_PublicationCreation(BaseModel):
    class Config:
        title = "Publication creation"
        original_path_id = "publication_creation"
    publication_creation_event: Annotated[AnyUrl, SPARQLBinding("?publication_creation_event")]


