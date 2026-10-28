\# IRIS WSG HE - Hesse Groundwater Protection Zones Ingestion



This module ingests Hesse groundwater protection zones from the HLNUG OGC WFS service (`https://gds.hessen.de/wfs/hlnug/wasserschutz`) into a PostGIS staging database.



\## Data Provenance

\* \*\*Source:\*\* Hessisches Landesamt für Naturschutz, Umwelt und Geologie (HLNUG)

\* \*\*Layer:\*\* `he\_wasserschutz\_zonen`

\* \*\*Transformation:\*\* Geometries are validated (invalid polygons repaired) and transformed to EPSG:25832.

\* \*\*Destination:\*\* `iris\_staging.water\_protection\_zones`



\## Assumptions \& Limitations

1\. \*\*Rate Limiting:\*\* The HLNUG WFS service has a 4000-record limit per request and may block rapid requests (HTTP 429). Paging is implemented, but a local fixture fallback (`fixtures/wfs\_features\_sample.gml`) is provided for demonstrative and testing purposes.

2\. \*\*Missing Attributes:\*\* Where extraction rates or update dates are absent in the source data, they are explicitly marked as `NULL`.

3\. \*\*Zone Mapping:\*\* Official zone codes are mapped strictly via a hardcoded dictionary (e.g., "I", "II", "IIIA"). No substring heuristics are used.



\## Run Instructions

1\. Ensure Docker Desktop is running.

2\. Run the pipeline and database:

&#x20;  ```bash

&#x20;  docker compose up --build

