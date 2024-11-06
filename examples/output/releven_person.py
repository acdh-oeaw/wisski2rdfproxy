from pydantic import BaseModel, AnyUrl
from rdfproxy import SPARQLBinding
from typing import Annotated

class Person(BaseModel):
    class Config:
        title = "Person"
        model_bool = "person"
        group_by = "person"
    person_appellation_assertion: Annotated[list[AnyUrl], SPARQLBinding("person__person_appellation_assertion")]
    person_descriptive_name: Annotated[list[str], SPARQLBinding("person__person_descriptive_name")]


