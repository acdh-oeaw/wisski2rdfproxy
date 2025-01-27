from pydantic import AnyUrl, BaseModel, Field  # noqa: F401
from rdfproxy import ConfigDict, SPARQLBinding
from typing import Annotated


class Publication_Publication_PublicationCreation(BaseModel):
    model_config = ConfigDict(
        title="Publication creation",
        model_bool="id",
    )
    id: Annotated[
        AnyUrl | None, SPARQLBinding("publication__publication__publication_creation")
    ] = Field(default=None, exclude=False)
    publication_creation_event: Annotated[
        AnyUrl,
        SPARQLBinding(
            "publication__publication__publication_creation__publication_creation_event"
        ),
    ]


class Publication_Publication(BaseModel):
    model_config = ConfigDict(
        title="Publication",
        model_bool="id",
        group_by="id",
    )
    id: Annotated[AnyUrl | None, SPARQLBinding("publication__publication")] = Field(
        default=None, exclude=False
    )
    publication_reference: Annotated[
        str, SPARQLBinding("publication__publication__publication_reference")
    ]
    publication_creation: Annotated[
        list[Publication_Publication_PublicationCreation],
        SPARQLBinding("publication__publication__publication_creation"),
    ]
