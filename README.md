# WissKAS 🐾

WissKI Adapter Serialization

## Rationale

WissKI pathbuilder defines (nested) models that are linked to RDF classes. By allowing fields to reference other pathbuilder models, it is possible to define recursive model structures. WissKAS provides:

- tools for parsing WissKI pathbuilder definitions (`wisskas.wisski`)
- tools for deriving limited depth submodels from those definitions (`wisskas.filter`)
- tools for generating [rdfproxy](https://github.com/acdh-oeaw/rdfproxy) endpoints from those models (`wisskas.serialize`)
- a command line tool for doing all of the above (`wisskas.main`)

