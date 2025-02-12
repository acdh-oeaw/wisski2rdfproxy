# WissKAS `≡UωU≡`

![tests](https://github.com/acdh-oeaw/wisskas/actions/workflows/tests.yml/badge.svg)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)

WissKI Adapter Serialization

## Rationale

WissKI pathbuilder defines (nested) models that are linked to RDF classes. By allowing fields to reference other pathbuilder models, it is possible to define recursive model structures. WissKAS provides:

- tools for parsing WissKI pathbuilder definitions (`wisskas.wisski`)
- tools for deriving limited depth submodels from those definitions (`wisskas.filter`)
- tools for generating [rdfproxy](https://github.com/acdh-oeaw/rdfproxy) endpoints from those models (`wisskas.serialize`)
- tools for generating SHACL shapes from the same models (`wisskas.shacl`)
- a command line tool for doing all of the above (`wisskas.main`)

