from pydantic import BaseModel, AnyUrl
from rdfproxy import SPARQLBinding

class BirthCircumstancesClaim(BaseModel):
    class Config:
        title = "Birth circumstances claim"
        original_path_id = "birth_circumstances_claim"



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
    person_gender_assertion: list[Annotated[PersonGenderAssertion, SPARQLBinding("?person_gender_assertion")]]
    person_ethnicity_assertion: list[Annotated[PersonEthnicityAssertion, SPARQLBinding("?person_ethnicity_assertion")]]
    person_descriptive_name: list[Annotated[str, SPARQLBinding("?person_descriptive_name")]]
    person_possession_assertion: list[Annotated[PersonPossessionAssertion, SPARQLBinding("?person_possession_assertion")]]
    person_status_assertion: list[Annotated[PersonStatusAssertion, SPARQLBinding("?person_status_assertion")]]
    person_religion_assertion: list[Annotated[PersonReligionAssertion, SPARQLBinding("?person_religion_assertion")]]
    person_occupation_assertion: list[Annotated[PersonOccupationAssertion, SPARQLBinding("?person_occupation_assertion")]]
    person_language_assertion: list[Annotated[PersonLanguageAssertion, SPARQLBinding("?person_language_assertion")]]
    person_kinship_assertion: list[Annotated[PersonKinshipAssertion, SPARQLBinding("?person_kinship_assertion")]]
    birth_circumstances_claim: Annotated[BirthCircumstancesClaim, SPARQLBinding("?birth_circumstances_claim")]
    person_death_assertion: Annotated[PersonDeathAssertion, SPARQLBinding("?person_death_assertion")]


class PersonDeathAssertion(BaseModel):
    class Config:
        title = "Death circumstances claim"
        original_path_id = "person_death_assertion"



class PersonEthnicityAssertion(BaseModel):
    class Config:
        title = "Ethnicity claim"
        original_path_id = "person_ethnicity_assertion"



class PersonGenderAssertion(BaseModel):
    class Config:
        title = "Gender assignment assertion"
        original_path_id = "person_gender_assertion"



class PersonKinshipAssertion(BaseModel):
    class Config:
        title = "Social relationship claim"
        original_path_id = "person_kinship_assertion"



class PersonLanguageAssertion(BaseModel):
    class Config:
        title = "Claim of language skill"
        original_path_id = "person_language_assertion"



class PersonOccupationAssertion(BaseModel):
    class Config:
        title = "Social Quality claim"
        original_path_id = "person_occupation_assertion"



class PersonPossessionAssertion(BaseModel):
    class Config:
        title = "Personal possession claim"
        original_path_id = "person_possession_assertion"



class PersonReligionAssertion(BaseModel):
    class Config:
        title = "Religious affiliation claim"
        original_path_id = "person_religion_assertion"



class PersonStatusAssertion(BaseModel):
    class Config:
        title = "Claim of social / legal status"
        original_path_id = "person_status_assertion"



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


