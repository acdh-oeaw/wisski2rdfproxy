from fastapi import FastAPI
from os import path
from rdfproxy import Page, SPARQLModelAdapter

app = FastAPI()

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


from releven_external_authority import ExternalAuthority
@app.get("/external_authority/")
def external_authority(page : int = 1, size : int = 10) -> Page[ExternalAuthority]:
    adapter = SPARQLModelAdapter(
        target="https://graphdb.r11.eu/repositories/RELEVEN",
        query=open(f"{path.dirname(path.realpath(__file__))}/releven_external_authority.rq").read().replace('\n ', ' '),
        model=ExternalAuthority)
    return adapter.query(page=page, size=size)


from releven_publication import Publication
@app.get("/publication/")
def publication(page : int = 1, size : int = 10) -> Page[Publication]:
    adapter = SPARQLModelAdapter(
        target="https://graphdb.r11.eu/repositories/RELEVEN",
        query=open(f"{path.dirname(path.realpath(__file__))}/releven_publication.rq").read().replace('\n ', ' '),
        model=Publication)
    return adapter.query(page=page, size=size)


from releven_boulloterion import Boulloterion
@app.get("/boulloterion/")
def boulloterion(page : int = 1, size : int = 10) -> Page[Boulloterion]:
    adapter = SPARQLModelAdapter(
        target="https://graphdb.r11.eu/repositories/RELEVEN",
        query=open(f"{path.dirname(path.realpath(__file__))}/releven_boulloterion.rq").read().replace('\n ', ' '),
        model=Boulloterion)
    return adapter.query(page=page, size=size)


from releven_person import Person
@app.get("/person/")
def person(page : int = 1, size : int = 10) -> Page[Person]:
    adapter = SPARQLModelAdapter(
        target="https://graphdb.r11.eu/repositories/RELEVEN",
        query=open(f"{path.dirname(path.realpath(__file__))}/releven_person.rq").read().replace('\n ', ' '),
        model=Person)
    return adapter.query(page=page, size=size)
