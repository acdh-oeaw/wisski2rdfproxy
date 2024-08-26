from pydantic import BaseModel, AnyUrl

class EthnicGroup(BaseModel):
    class Config:
        title = "Ethnic Group"
    ethnic_group_name: str


class Publication(BaseModel):
    class Config:
        title = "Publication"
    publication_reference: str
    publication_creation: list[PublicationCreation]
    publication_text_assertion: list[PublicationTextAssertion]


class PersonReligionAssertion(BaseModel):
    class Config:
        title = "Religious affiliation claim"
    person_religion: Religion
    person_religion_by: Person
    person_religion_by_6469fc34bfcc0: AuthorList
    person_religion_source: Source


class PersonAppellationAssertion(BaseModel):
    class Config:
        title = "Name(s) in the sources"
    person_appellation_by: Person
    person_appellation_source: Source
    person_appellation_is: str
    person_appellation_by_64676fe68daa0: AuthorList


class PersonPersonOccupationAssertion(BaseModel):
    class Config:
        title = "Social Quality claim"
    person_occupation_is: SocialQuality
    person_occupation_by: Person
    person_occupation_by_646a02fb8ea01: AuthorList
    person_occupation_source: Source


class PersonPersonLanguageAssertion(BaseModel):
    class Config:
        title = "Claim of language skill"
    person_language_by: Person
    person_language_by_646a0ccab122a: AuthorList
    person_language_source: Source
    person_language_skill: PersonLanguageSkill


class PublicationTextAssertion(BaseModel):
    class Config:
        title = "Publication text assertion"
    publication_text_is: WrittenWork


class PersonBirthCircumstancesClaimBirthEventDescriptionOfBirth(BaseModel):
    class Config:
        title = "Description of birth"
    birth_description_is: str
    birth_description_source: Source
    birth_description_by: Person
    birth_description_by_65d726f3d6630: AuthorList


class KinshipType(BaseModel):
    class Config:
        title = "Social relationship type"
    kinship_label: str
    social_relationship_category: list[str]


class Person(BaseModel):
    class Config:
        title = "Person"
    person_id_assignment: list[PersonIdAssignment]
    person_appellation_assertion: list[PersonAppellationAssertion]
    person_gender_assertion: list[PersonGenderAssertion]
    person_ethnicity_assertion: list[PersonEthnicityAssertion]
    person_descriptive_name: list[str]
    person_possession_assertion: list[PersonPossessionAssertion]
    person_status_assertion: list[PersonStatusAssertion]
    person_religion_assertion: list[PersonReligionAssertion]
    person_occupation_assertion: list[PersonOccupationAssertion]
    person_language_assertion: list[PersonLanguageAssertion]
    person_kinship_assertion: list[PersonKinshipAssertion]
    birth_circumstances_claim: BirthCircumstancesClaim
    person_death_assertion: PersonDeathAssertion


class PersonBirthCircumstancesClaimBirthEventBirthTemporalAssertion(BaseModel):
    class Config:
        title = "Time frame of birth"
    birth_timespan_is: str
    birth_timespan_by: Person
    birth_timespan_by_65d72a51e9f30: AuthorList
    birth_timespan_source: Source


class PersonPersonDeathAssertionPersonDeathDeathDescriptionAssertion(BaseModel):
    class Config:
        title = "Description of death"
    death_description_is: str
    death_description_by: Person
    death_description_by_646a679998b7f: AuthorList
    death_description_source: Source


class PersonPersonDeathAssertionPersonDeathDeathTemporalAssertion(BaseModel):
    class Config:
        title = "Time frame of death"
    death_timespan_is: str
    death_timespan_by: Person
    death_timespan_by_646a694b4a6ce: AuthorList
    death_timespan_source: Source


class PersonPersonKinshipAssertion(BaseModel):
    class Config:
        title = "Social relationship claim"
    person_kinship_by: Person
    person_kinship_by_646a12fe51e59: AuthorList
    person_kinship_source: Source
    person_kinship: PersonKinship


class LegalStatus(BaseModel):
    class Config:
        title = "Social Role (C12)"
    legal_status_label: str


class ExternalAuthority(BaseModel):
    class Config:
        title = "External Authority"
    external_authority_display_name: str
    external_authority_url: AnyUrl


class PersonIdAssignment(BaseModel):
    class Config:
        title = "Identity in other services"
    person_identifier_by: ExternalAuthority
    person_identifier: PersonIdentifier


class Person(BaseModel):
    class Config:
        title = "Person"
    person_id_assignment: list[PersonIdAssignment]
    person_appellation_assertion: list[PersonAppellationAssertion]
    person_gender_assertion: list[PersonGenderAssertion]
    person_ethnicity_assertion: list[PersonEthnicityAssertion]
    person_descriptive_name: list[str]
    person_possession_assertion: list[PersonPossessionAssertion]
    person_status_assertion: list[PersonStatusAssertion]
    person_religion_assertion: list[PersonReligionAssertion]
    person_occupation_assertion: list[PersonOccupationAssertion]
    person_language_assertion: list[PersonLanguageAssertion]
    person_kinship_assertion: list[PersonKinshipAssertion]
    birth_circumstances_claim: BirthCircumstancesClaim
    person_death_assertion: PersonDeathAssertion


class PersonPersonStatusAssertionPersonSocialRole(BaseModel):
    class Config:
        title = "person_social_role"
    person_status_is: LegalStatus
    person_status_is_654d573e558ad: str


class PersonGenderDesignation(BaseModel):
    class Config:
        title = "Gender assignment"
    person_gender_assignment: Gender
    gender_timeframe_assertion: str


class PersonBirthCircumstancesClaim(BaseModel):
    class Config:
        title = "Birth circumstances claim"
    birth_event: BirthEvent


class PersonStatusAssertion(BaseModel):
    class Config:
        title = "Claim of social / legal status"
    person_status_authority: Person
    person_status_tsource: Source
    person_status_authority_6469faa26a323: AuthorList
    person_social_role: PersonSocialRole


class PersonSocialRole(BaseModel):
    class Config:
        title = "person_social_role"
    person_status_is: LegalStatus
    person_status_is_654d573e558ad: str


class ExternalAuthority(BaseModel):
    class Config:
        title = "External Authority"
    external_authority_display_name: str
    external_authority_url: AnyUrl


class TextCreationTimeframeAssertio(BaseModel):
    class Config:
        title = "text_creation_timeframe_assertion"
    text_creation_timeframe_is: str
    text_creation_timeframe_is_654d5928e55a3: Person
    text_creation_timeframe_is_654d596b0ff30: AuthorList
    text_creation_timeframe_is_654d596b0ff30_654d59d5a1545: Source


class PersonEthnicityAssertion(BaseModel):
    class Config:
        title = "Ethnicity claim"
    person_ethnicity_by: Person
    person_ethnicity_source: Source
    person_ethnicity_is: EthnicGroup
    person_ethnicity_by_64679cd48693f: AuthorList


class PersonPersonIdAssignment(BaseModel):
    class Config:
        title = "Identity in other services"
    person_identifier_by: ExternalAuthority
    person_identifier: PersonIdentifier


class WorkCreation6464E7F7408F5(BaseModel):
    class Config:
        title = "text_creation_author_assertion"
    work_creation_6464e7f7408f5_6464e84c560ab: Person
    work_creation_6464e7f7408f5_6464e84c560ab_6464eedea54c2: Person
    work_creation_6464e7f7408f5_6464e84c560ab_6464eedea54c2_64676dec838f6: AuthorList
    work_creation_6464e7f7408f5_6464e84c560ab_646770ec2f59a: AuthorList


class AuthorList(BaseModel):
    class Config:
        title = "Author list"
    author_list_members: list[Person]
    author_list_namestring: str


class PersonPersonAppellationAssertion(BaseModel):
    class Config:
        title = "Name(s) in the sources"
    person_appellation_by: Person
    person_appellation_source: Source
    person_appellation_is: str
    person_appellation_by_64676fe68daa0: AuthorList


class PersonPersonDeathAssertion(BaseModel):
    class Config:
        title = "Death circumstances claim"
    person_death: PersonDeath


class PersonKinshipAssertion(BaseModel):
    class Config:
        title = "Social relationship claim"
    person_kinship_by: Person
    person_kinship_by_646a12fe51e59: AuthorList
    person_kinship_source: Source
    person_kinship: PersonKinship


class PersonPersonGenderAssertion(BaseModel):
    class Config:
        title = "Gender assignment assertion"
    person_gender_by: Person
    person_gender_by_6469f837afcca: ExternalAuthority
    gender_assignment_source: Source
    person_gender_designation: PersonGenderDesignation


class PersonPersonEthnicityAssertion(BaseModel):
    class Config:
        title = "Ethnicity claim"
    person_ethnicity_by: Person
    person_ethnicity_source: Source
    person_ethnicity_is: EthnicGroup
    person_ethnicity_by_64679cd48693f: AuthorList


class Source(BaseModel):
    class Config:
        title = "Source"
    source_publication: Publication
    source_seal: Boulloterion
    source_reference: str
    source_content: str


class Gender(BaseModel):
    class Config:
        title = "Gender"
    gender_label: str


class SocialQuality(BaseModel):
    class Config:
        title = "Social Quality (C2)"
    social_quality_label: str


class PersonPersonIdAssignmentPersonIdentifier(BaseModel):
    class Config:
        title = "External identifier"
    person_identifier_is: AnyUrl
    person_identifier_plain: str


class PersonKinship(BaseModel):
    class Config:
        title = "Kinship relation"
    person_kinship_type: KinshipType
    person_kinship_kin: Person
    person_kinship_type_654d55427c0eb: str


class BirthCircumstancesClaim(BaseModel):
    class Config:
        title = "Birth circumstances claim"
    birth_event: BirthEvent


class PersonLanguageSkill(BaseModel):
    class Config:
        title = "Language skill"
    person_language_known: Language
    person_language_known_654d55d4cef6f: str


class PersonGenderAssertion(BaseModel):
    class Config:
        title = "Gender assignment assertion"
    person_gender_by: Person
    person_gender_by_6469f837afcca: ExternalAuthority
    gender_assignment_source: Source
    person_gender_designation: PersonGenderDesignation


class Religion(BaseModel):
    class Config:
        title = "Religion"
    religion_label: str


class DescriptionOfBirth(BaseModel):
    class Config:
        title = "Description of birth"
    birth_description_is: str
    birth_description_source: Source
    birth_description_by: Person
    birth_description_by_65d726f3d6630: AuthorList


class PersonPersonPossessionAssertion(BaseModel):
    class Config:
        title = "Personal possession claim"
    possession_assertion_authority: Person
    possession_assertion_source: Source
    possession_assertion_is: str
    possession_assertion_authority_6469fa3852d6e: AuthorList


class PersonBirthCircumstancesClaimBirthEvent(BaseModel):
    class Config:
        title = "Birth event"
    description_of_birth: list[DescriptionOfBirth]
    birth_temporal_assertion: list[BirthTemporalAssertion]


class Language(BaseModel):
    class Config:
        title = "Language"
    language_name: list[str]


class PersonPersonLanguageAssertionPersonLanguageSkill(BaseModel):
    class Config:
        title = "Language skill"
    person_language_known: Language
    person_language_known_654d55d4cef6f: str


class PersonDeath(BaseModel):
    class Config:
        title = "Death event"
    death_description_assertion: list[DeathDescriptionAssertion]
    death_temporal_assertion: list[DeathTemporalAssertion]


class BoulloterionIdentifierAssignme(BaseModel):
    class Config:
        title = "boulloterion_identifier_assignment"
    boulloterion_identifier_by: ExternalAuthority
    boulloterion_identifier: list[BoulloterionIdentifier]


class DeathDescriptionAssertion(BaseModel):
    class Config:
        title = "Description of death"
    death_description_is: str
    death_description_by: Person
    death_description_by_646a679998b7f: AuthorList
    death_description_source: Source


class PersonLanguageAssertion(BaseModel):
    class Config:
        title = "Claim of language skill"
    person_language_by: Person
    person_language_by_646a0ccab122a: AuthorList
    person_language_source: Source
    person_language_skill: PersonLanguageSkill


class BirthTemporalAssertion(BaseModel):
    class Config:
        title = "Time frame of birth"
    birth_timespan_is: str
    birth_timespan_by: Person
    birth_timespan_by_65d72a51e9f30: AuthorList
    birth_timespan_source: Source


class WorkCreation(BaseModel):
    class Config:
        title = "text_creation"
    work_creation_6464e7f7408f5: list[WorkCreation6464E7F7408F5]
    text_creation_timeframe_assertio: TextCreationTimeframeAssertio


class Boulloterion(BaseModel):
    class Config:
        title = "Boulloterion"
    boulloterion_identifier_assignme: list[BoulloterionIdentifierAssignme]
    boulloterion_seal_assertion: list[BoulloterionSealAssertion]
    boulloterion_description: str


class PersonPersonStatusAssertion(BaseModel):
    class Config:
        title = "Claim of social / legal status"
    person_status_authority: Person
    person_status_tsource: Source
    person_status_authority_6469faa26a323: AuthorList
    person_social_role: PersonSocialRole


class WorkCreationAssertion(BaseModel):
    class Config:
        title = "text_creation_assertion"
    work_creation: WorkCreation
    work_creation_assertion_by: Person
    work_creation_assertion_by_64676da87229e: AuthorList


class PersonPossessionAssertion(BaseModel):
    class Config:
        title = "Personal possession claim"
    possession_assertion_authority: Person
    possession_assertion_source: Source
    possession_assertion_is: str
    possession_assertion_authority_6469fa3852d6e: AuthorList


class DeathTemporalAssertion(BaseModel):
    class Config:
        title = "Time frame of death"
    death_timespan_is: str
    death_timespan_by: Person
    death_timespan_by_646a694b4a6ce: AuthorList
    death_timespan_source: Source


class PersonOccupationAssertion(BaseModel):
    class Config:
        title = "Social Quality claim"
    person_occupation_is: SocialQuality
    person_occupation_by: Person
    person_occupation_by_646a02fb8ea01: AuthorList
    person_occupation_source: Source


class BirthEvent(BaseModel):
    class Config:
        title = "Birth event"
    description_of_birth: list[DescriptionOfBirth]
    birth_temporal_assertion: list[BirthTemporalAssertion]


class PersonPersonGenderAssertionPersonGenderDesignation(BaseModel):
    class Config:
        title = "Gender assignment"
    person_gender_assignment: Gender
    gender_timeframe_assertion: str


class PersonDeathAssertion(BaseModel):
    class Config:
        title = "Death circumstances claim"
    person_death: PersonDeath


class PersonPersonKinshipAssertionPersonKinship(BaseModel):
    class Config:
        title = "Kinship relation"
    person_kinship_type: KinshipType
    person_kinship_kin: Person
    person_kinship_type_654d55427c0eb: str


class PublicationCreation(BaseModel):
    class Config:
        title = "Publication creation"
    publication_creation_event: PublicationCreationEvent


class PersonPersonReligionAssertion(BaseModel):
    class Config:
        title = "Religious affiliation claim"
    person_religion: Religion
    person_religion_by: Person
    person_religion_by_6469fc34bfcc0: AuthorList
    person_religion_source: Source


class BoulloterionSealAssertion(BaseModel):
    class Config:
        title = "boulloterion_seal_assertion"
    boulloterion_seal_by: Person
    boulloterion_produced_seal: None
    boulloterion_seal_by_6606a275376d5: AuthorList
    boulloterion_seal_source: Source


class PublicationCreationEvent(BaseModel):
    class Config:
        title = "publication_creation_event"
    pub_creation_event_by_assertion: Person
    pub_creation_event_by_assertion_64676c6b5bd33: AuthorList


class PersonPersonDeathAssertionPersonDeath(BaseModel):
    class Config:
        title = "Death event"
    death_description_assertion: list[DeathDescriptionAssertion]
    death_temporal_assertion: list[DeathTemporalAssertion]


class BoulloterionIdentifier(BaseModel):
    class Config:
        title = "External identifier"
    boulloterion_identifier_is: str
    boulloterion_identifier_is_6606afa045f10: AnyUrl


class PersonIdentifier(BaseModel):
    class Config:
        title = "External identifier"
    person_identifier_is: AnyUrl
    person_identifier_plain: str


class WrittenWork(BaseModel):
    class Config:
        title = "Text Expression"
    written_work_label: str
    work_creation_assertion: list[WorkCreationAssertion]


