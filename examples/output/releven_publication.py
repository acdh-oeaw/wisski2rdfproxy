from pydantic import BaseModel, AnyUrl
from rdfproxy import SPARQLBinding

class ExternalAuthority(BaseModel):
    class Config:
        title = "External Authority"
        original_path_id = "external_authority"
    external_authority_display_name: Annotated[str, SPARQLBinding("?external_authority__external_authority_display_name")]
    external_authority_url: Annotated[AnyUrl, SPARQLBinding("?external_authority__external_authority_url")]


class Person(BaseModel):
    class Config:
        title = "Person"
        original_path_id = "person"
    person_id_assignment: list[Annotated[Person_PersonIdAssignment, SPARQLBinding("?person__person_id_assignment")]]
    person_gender_assertion: list[Annotated[AnyUrl, SPARQLBinding("?person__person_gender_assertion")]]
    person_ethnicity_assertion: list[Annotated[AnyUrl, SPARQLBinding("?person__person_ethnicity_assertion")]]
    person_descriptive_name: list[Annotated[str, SPARQLBinding("?person__person_descriptive_name")]]
    person_possession_assertion: list[Annotated[AnyUrl, SPARQLBinding("?person__person_possession_assertion")]]
    person_status_assertion: list[Annotated[AnyUrl, SPARQLBinding("?person__person_status_assertion")]]
    person_religion_assertion: list[Annotated[AnyUrl, SPARQLBinding("?person__person_religion_assertion")]]
    person_occupation_assertion: list[Annotated[AnyUrl, SPARQLBinding("?person__person_occupation_assertion")]]
    person_language_assertion: list[Annotated[AnyUrl, SPARQLBinding("?person__person_language_assertion")]]
    person_kinship_assertion: list[Annotated[AnyUrl, SPARQLBinding("?person__person_kinship_assertion")]]
    birth_circumstances_claim: Annotated[Person_BirthCircumstancesClaim, SPARQLBinding("?person__birth_circumstances_claim")]
    person_death_assertion: Annotated[Person_PersonDeathAssertion, SPARQLBinding("?person__person_death_assertion")]


class Person_BirthCircumstancesClaim(BaseModel):
    class Config:
        title = "Birth circumstances claim"
        original_path_id = "birth_circumstances_claim"
    birth_event: Annotated[Person_BirthCircumstancesClaim_BirthEvent, SPARQLBinding("?person__birth_circumstances_claim__birth_event")]


class Person_BirthCircumstancesClaim_BirthEvent(BaseModel):
    class Config:
        title = "Birth event"
        original_path_id = "birth_event"
    description_of_birth: list[Annotated[Person_BirthCircumstancesClaim_BirthEvent_DescriptionOfBirth, SPARQLBinding("?person__birth_circumstances_claim__birth_event__description_of_birth")]]
    birth_temporal_assertion: list[Annotated[Person_BirthCircumstancesClaim_BirthEvent_BirthTemporalAssertion, SPARQLBinding("?person__birth_circumstances_claim__birth_event__birth_temporal_assertion")]]


class Person_BirthCircumstancesClaim_BirthEvent_BirthTemporalAssertion(BaseModel):
    class Config:
        title = "Time frame of birth"
        original_path_id = "birth_temporal_assertion"
    birth_timespan_is: Annotated[str, SPARQLBinding("?person__birth_circumstances_claim__birth_event__birth_temporal_assertion__birth_timespan_is")]
    birth_timespan_source: Annotated[AnyUrl, SPARQLBinding("?person__birth_circumstances_claim__birth_event__birth_temporal_assertion__birth_timespan_source")]


class Person_BirthCircumstancesClaim_BirthEvent_DescriptionOfBirth(BaseModel):
    class Config:
        title = "Description of birth"
        original_path_id = "description_of_birth"
    birth_description_is: Annotated[str, SPARQLBinding("?person__birth_circumstances_claim__birth_event__description_of_birth__birth_description_is")]
    birth_description_source: Annotated[AnyUrl, SPARQLBinding("?person__birth_circumstances_claim__birth_event__description_of_birth__birth_description_source")]
    birth_description_by: Annotated[AnyUrl, SPARQLBinding("?person__birth_circumstances_claim__birth_event__description_of_birth__birth_description_by")]


class Person_PersonDeathAssertion(BaseModel):
    class Config:
        title = "Death circumstances claim"
        original_path_id = "person_death_assertion"
    person_death: Annotated[Person_PersonDeathAssertion_PersonDeath, SPARQLBinding("?person__person_death_assertion__person_death")]


class Person_PersonDeathAssertion_PersonDeath(BaseModel):
    class Config:
        title = "Death event"
        original_path_id = "person_death"
    death_description_assertion: list[Annotated[AnyUrl, SPARQLBinding("?person__person_death_assertion__person_death__death_description_assertion")]]
    death_temporal_assertion: list[Annotated[AnyUrl, SPARQLBinding("?person__person_death_assertion__person_death__death_temporal_assertion")]]


class Person_PersonIdAssignment(BaseModel):
    class Config:
        title = "Identity in other services"
        original_path_id = "person_id_assignment"
    person_identifier_by: Annotated[Person_PersonIdAssignment_PersonIdentifierBy, SPARQLBinding("?person__person_id_assignment__person_identifier_by")]
    person_identifier: Annotated[Person_PersonIdAssignment_PersonIdentifier, SPARQLBinding("?person__person_id_assignment__person_identifier")]


class Person_PersonIdAssignment_PersonIdentifier(BaseModel):
    class Config:
        title = "External identifier"
        original_path_id = "person_identifier"
    person_identifier_is: Annotated[AnyUrl, SPARQLBinding("?person__person_id_assignment__person_identifier__person_identifier_is")]
    person_identifier_plain: Annotated[str, SPARQLBinding("?person__person_id_assignment__person_identifier__person_identifier_plain")]


class Person_PersonIdAssignment_PersonIdentifierBy(BaseModel):
    class Config:
        title = "External Authority"
        original_path_id = "external_authority"
    external_authority_display_name: Annotated[str, SPARQLBinding("?person__person_id_assignment__person_identifier_by__external_authority_display_name")]
    external_authority_url: Annotated[AnyUrl, SPARQLBinding("?person__person_id_assignment__person_identifier_by__external_authority_url")]


class Publication(BaseModel):
    class Config:
        title = "Publication"
        original_path_id = "publication"
    publication_reference: Annotated[str, SPARQLBinding("?publication__publication_reference")]
    publication_creation: list[Annotated[Publication_PublicationCreation, SPARQLBinding("?publication__publication_creation")]]


class Publication_PublicationCreation(BaseModel):
    class Config:
        title = "Publication creation"
        original_path_id = "publication_creation"
    publication_creation_event: Annotated[AnyUrl, SPARQLBinding("?publication__publication_creation__publication_creation_event")]


