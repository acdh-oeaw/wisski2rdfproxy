from fastapi import FastAPI, Query
from os import path
from rdfproxy import Page, QueryParameters, SPARQLModelAdapter
from typing import Annotated

app = FastAPI()

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
from git import Repo


# The automatic health check endpoint is /. The return code has to be 200 or 30x.
@app.get("/")
def version():
    repo = Repo(search_parent_directories=True)
    return {"version": repo.git.describe(tags=True, dirty=True, always=True)}


from releven_external_authority import ExternalAuthority


@app.get("/external_authority")
def external_authority(
    params: Annotated[QueryParameters, Query()],
) -> Page[ExternalAuthority]:
    adapter = SPARQLModelAdapter(
        target="https://graphdb.r11.eu/repositories/RELEVEN",
        query=open(
            f"{path.dirname(path.realpath(__file__))}/releven_external_authority.rq"
        )
        .read()
        .replace("\n ", " "),
        model=ExternalAuthority,
    )
    return adapter.query(params)


from releven_publication import Publication


@app.get("/publication")
def publication(params: Annotated[QueryParameters, Query()]) -> Page[Publication]:
    adapter = SPARQLModelAdapter(
        target="https://graphdb.r11.eu/repositories/RELEVEN",
        query=open(f"{path.dirname(path.realpath(__file__))}/releven_publication.rq")
        .read()
        .replace("\n ", " "),
        model=Publication,
    )
    return adapter.query(params)


from releven_boulloterion import Boulloterion


@app.get("/boulloterion")
def boulloterion(params: Annotated[QueryParameters, Query()]) -> Page[Boulloterion]:
    adapter = SPARQLModelAdapter(
        target="https://graphdb.r11.eu/repositories/RELEVEN",
        query=open(f"{path.dirname(path.realpath(__file__))}/releven_boulloterion.rq")
        .read()
        .replace("\n ", " "),
        model=Boulloterion,
    )
    return adapter.query(params)


from releven_person import Person


@app.get("/person")
def person(params: Annotated[QueryParameters, Query()]) -> Page[Person]:
    adapter = SPARQLModelAdapter(
        target="https://graphdb.r11.eu/repositories/RELEVEN",
        query=open(f"{path.dirname(path.realpath(__file__))}/releven_person.rq")
        .read()
        .replace("\n ", " "),
        model=Person,
    )
    return adapter.query(params)
