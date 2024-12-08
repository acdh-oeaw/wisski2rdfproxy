
from os import path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from git import Repo
from rdfproxy import Page, QueryParameters, SPARQLModelAdapter
from releven_boulloterion import Boulloterion
from releven_external_authority import ExternalAuthority
from releven_person import Person
from releven_publication import Publication

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# The automatic health check endpoint is /. The return code has to be 200 or 30x.
@app.get("/")
def version():
    repo = Repo(search_parent_directories=True)
    return {"version": repo.git.describe(tags=True, dirty=True, always=True)}


@app.get("/external_authority")
def external_authority(page: int = 1, size: int = 10) -> Page[ExternalAuthority]:
    adapter = SPARQLModelAdapter(
        target="https://graphdb.r11.eu/repositories/RELEVEN",
        query=open(
            f"{path.dirname(path.realpath(__file__))}/releven_external_authority.rq").read().replace('\n ', ' '),
        model=ExternalAuthority)
    parameters = QueryParameters(page=page, size=size)
    return adapter.query(parameters)


@app.get("/publication")
def publication(page: int = 1, size: int = 10) -> Page[Publication]:
    adapter = SPARQLModelAdapter(
        target="https://graphdb.r11.eu/repositories/RELEVEN",
        query=open(
            f"{path.dirname(path.realpath(__file__))}/releven_publication.rq").read().replace('\n ', ' '),
        model=Publication)
    parameters = QueryParameters(page=page, size=size)
    return adapter.query(parameters)


@app.get("/boulloterion")
def boulloterion(page: int = 1, size: int = 10) -> Page[Boulloterion]:
    adapter = SPARQLModelAdapter(
        target="https://graphdb.r11.eu/repositories/RELEVEN",
        query=open(
            f"{path.dirname(path.realpath(__file__))}/releven_boulloterion.rq").read().replace('\n ', ' '),
        model=Boulloterion)
    parameters = QueryParameters(page=page, size=size)
    return adapter.query(parameters)


@app.get("/person")
def person(page: int = 1, size: int = 10) -> Page[Person]:
    adapter = SPARQLModelAdapter(
        target="https://graphdb.r11.eu/repositories/RELEVEN",
        query=open(
            f"{path.dirname(path.realpath(__file__))}/releven_person.rq").read().replace('\n ', ' '),
        model=Person)
    parameters = QueryParameters(page=page, size=size)
    return adapter.query(parameters)

