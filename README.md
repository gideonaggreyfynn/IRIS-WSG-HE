# 🗺️ IRIS WSG HE - Hesse Groundwater Protection Zones Ingestion

## 📖 Overview
This repository contains a robust ETL (Extract, Transform, Load) pipeline designed to ingest Hesse groundwater protection zones from the HLNUG OGC WFS service into an isolated PostGIS staging database. 

Built to support site-permitting and groundwater restriction screening, this module ensures data traceability, spatial accuracy, and idempotent loading.

## ✨ Key Features
*   **Resilient Data Acquisition:** Implements OGC WFS paging and includes an automated fallback to a local fixture (`wfs_features_sample.gml`) if the live service rate-limits (HTTP 429).
*   **Strict Classification Mapping:** Official zone codes are mapped using a strict, traceable dictionary—no fragile substring heuristics.
*   **Geospatial Integrity:** Automatically detects and repairs invalid multipart polygons and transforms geometries to `EPSG:25832`.
*   **Idempotent Database Loading:** Utilizes PostgreSQL's `ON CONFLICT DO UPDATE` to ensure running the pipeline multiple times updates records rather than creating duplicates.

## 📂 Project Structure
```text
IRIS-WSG-HE/
├── app/                  # Core logic (WFS client, mapping, validation, loader)
├── fixtures/             # Mock GML data for offline demonstration
├── scripts/              # Quality report generation
├── tests/                # Automated pytest suite
├── Dockerfile            # Python environment container
├── docker-compose.yml    # Multi-container setup (PostGIS + Ingest)
├── init.sql              # Database schema initialization
└── main.py               # Pipeline entry point

📋 Requirements
Docker Desktop & Docker Compose
PostgreSQL 16 with PostGIS 3.4 (automatically handled by Docker)
Python 3.11+ (if running tests locally)
Git

📥 Clone the Repository
cmd:
git clone https://github.com/gideonaggreyfynn/IRIS-WSG-HE.git
cd IRIS-WSG-HE

📊 Data Provenance
Source: Hessisches Landesamt für Naturschutz, Umwelt und Geologie (HLNUG)
Endpoint: https://gds.hessen.de/wfs/hlnug/wasserschutz
Layer: he_wasserschutz_zonen
Transformation: Validated and transformed to EPSG:25832.
Destination: iris_staging.water_protection_zones

🗺️ Schema Mapping
To satisfy the acceptance criteria (no fragile substring rules), the source attributes are mapped strictly using a dictionary lookup in app/schema_mapping.py:

Source Code	Mapped Restriction Category
I, 1		Zone I
II, 2, 2o	Zone II
III, 3		Zone III
IIIA		Zone IIIA
IIIB		Zone IIIB
Any other value	Unknown (explicitly flagged)

⚠️ Assumptions & Limitations
Rate Limiting: The HLNUG WFS service limits requests and may block rapid access. 
The fixture fallback is provided to  ensure reproducible testing without bypassing server restrictions.
Missing Attributes: Where extraction rates or update dates are absent in the source data, they are explicitly stored as NULL.
Staging Only: This module strictly writes to the iris_staging schema and does not interact with production systems (iris_core).

🚀 Run Instructions
Prerequisite: Ensure Docker Desktop is running.

1. Start the database and run the ingestion pipeline:
cmd:
docker compose up -d --build

(The pipeline will wait for the database to be healthy, run the init.sql script to create the schema, and execute 
the ingestion. The -d flag runs it in the background so you keep your terminal prompt).

2. Wait for Ingestion to Complete:
Since it runs in the background, you can verify the ingestion finished successfully by running:
cmd:
docker compose logs ingest

(Wait until you see Ingestion complete: 2 records upserted and exited with code 0).

3. Validation Query:
Prove the data was loaded correctly by running this query directly inside the running Docker container. 

*(Note: Ensure you copy and paste this as a single continuous line):*
cmd:
docker exec -it iris-staging-db psql -U postgres -d iris_staging -c "SELECT source_zone_id, restriction_category, ST_AsText(geometry) FROM iris_staging.water_protection_zones LIMIT 5;"

🧪 Automated Testing
The project includes a pytest suite covering schema mapping and geometry repairs, using the representative fixture data.

1. Create and activate a virtual environment:
cmd:
python -m venv .venv
.venv\Scripts\activate

2. Install development dependencies:
cmd:
pip install -e ".[dev]"

3. Generate the Quality/Error Report:
cmd:
python -m scripts.quality_report
(This will output quality_report.json directly into your project folder).

4. Run the tests:
cmd:
python -m pytest
Expect all 6 tests to pass.

5. Clean up:
When finished, shut down the background containers to free up system resources:
cmd:
docker compose down

