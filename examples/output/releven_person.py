from pydantic import AnyUrl, BaseModel, Field  # noqa: F401
from rdfproxy import ConfigDict, SPARQLBinding
from typing import Annotated


class Person(BaseModel):
    model_config = ConfigDict(
        title="Person",
        model_bool="id",
        group_by="id",
    )
    id: Annotated[AnyUrl | None, SPARQLBinding("person")] = Field(
        default=None, exclude=False
    )
    person_id_assignment: Annotated[
        list[AnyUrl], SPARQLBinding("person__person_id_assignment")
    ]
    person_appellation_assertion: Annotated[
        list[AnyUrl], SPARQLBinding("person__person_appellation_assertion")
    ]
    person_gender_assertion: Annotated[
        list[AnyUrl], SPARQLBinding("person__person_gender_assertion")
    ]
    person_ethnicity_assertion: Annotated[
        list[AnyUrl], SPARQLBinding("person__person_ethnicity_assertion")
    ]
    person_descriptive_name: Annotated[
        list[str], SPARQLBinding("person__person_descriptive_name")
    ]
    person_possession_assertion: Annotated[
        list[AnyUrl], SPARQLBinding("person__person_possession_assertion")
    ]
    person_status_assertion: Annotated[
        list[AnyUrl], SPARQLBinding("person__person_status_assertion")
    ]
    person_religion_assertion: Annotated[
        list[AnyUrl], SPARQLBinding("person__person_religion_assertion")
    ]
    person_occupation_assertion: Annotated[
        list[AnyUrl], SPARQLBinding("person__person_occupation_assertion")
    ]
    person_language_assertion: Annotated[
        list[AnyUrl], SPARQLBinding("person__person_language_assertion")
    ]
    person_kinship_assertion: Annotated[
        list[AnyUrl], SPARQLBinding("person__person_kinship_assertion")
    ]
    birth_circumstances_claim: Annotated[
        AnyUrl, SPARQLBinding("person__birth_circumstances_claim")
    ]
    person_death_assertion: Annotated[
        AnyUrl, SPARQLBinding("person__person_death_assertion")
    ]
