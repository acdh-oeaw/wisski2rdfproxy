from fastapi import FastAPI
from os import path
from rdfproxy import Page, SPARQLModelAdapter

app = FastAPI()

from releven_external_authority import ExternalAuthority
@app.get("/external_authority/")
def external_authority():
  adapter = SPARQLModelAdapter(
    target="https://graphdb.r11.eu/repositories/RELEVEN",
    query=open(f"{path.dirname(path.realpath(__file__))}/releven_external_authority.rq").read(),
    model=ExternalAuthority)
  return adapter.query()


from releven_publication import Publication
@app.get("/publication/")
def publication():
  adapter = SPARQLModelAdapter(
    target="https://graphdb.r11.eu/repositories/RELEVEN",
    query=open(f"{path.dirname(path.realpath(__file__))}/releven_publication.rq").read(),
    model=Publication)
  return adapter.query()


from releven_person import Person
@app.get("/person/")
def person():
  adapter = SPARQLModelAdapter(
    target="https://graphdb.r11.eu/repositories/RELEVEN",
    query=open(f"{path.dirname(path.realpath(__file__))}/releven_person.rq").read(),
    model=Person)
  return adapter.query()
