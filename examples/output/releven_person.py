from typing import Annotated

from pydantic import AnyUrl, BaseModel, Field  # noqa: F401
from rdfproxy import ConfigDict, SPARQLBinding


class Person(BaseModel):
    model_config = ConfigDict(title="Person",
                              model_bool="id",
                              group_by="id",)
    id: Annotated[AnyUrl | None, SPARQLBinding(
        "person")] = Field(default=None, exclude=True)
    person_appellation_assertion: Annotated[list[AnyUrl], SPARQLBinding(
        "person__person_appellation_assertion")]
    person_descriptive_name: Annotated[list[str], SPARQLBinding(
        "person__person_descriptive_name")]

