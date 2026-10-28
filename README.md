# 🗺️ IRIS WSG HE - Hesse Groundwater Protection Zones Ingestion

## 📖 Overview
This repository contains a robust ETL (Extract, Transform, Load) pipeline designed to ingest Hesse groundwater protection zones from the HLNUG OGC WFS service into an isolated PostGIS staging database. 

Built to support site-permitting and groundwater restriction screening, this module ensures data traceability, spatial accuracy, and idempotent loading.

## ✨ Key Features
*   **Resilient Data Acquisition:** Implements OGC WFS paging and includes an automated fallback to a local fixture (`wfs_features_sample.gml`) if the live service rate-limits (HTTP 429).
*   **Strict Classification Mapping:** Official zone codes (e.g., "I", "II", "IIIA") are mapped using a strict, traceable dictionary—no fragile substring heuristics.
*   **Geospatial Integrity:** Automatically detects and repairs invalid multipart polygons and transforms geometries to `EPSG:25832`.
*   **Idempotent Database Loading:** Utilizes PostgreSQL's `ON CONFLICT DO UPDATE` to ensure running the pipeline multiple times updates records rather than creating duplicates.

## 🏗️ System Architecture
The pipeline follows a standard ETL flow, orchestrated via Docker Compose:

```mermaid
graph TD
    A[HLNUG WFS Server or Local Fixture] -->|Extract: Raw GML| B(app/wfs_client.py)
    B -->|Parse XML| C(main.py)
    C -->|Transform: Map Zones| D(app/schema_mapping.py)
    C -->|Transform: Repair Geometry| E(app/validation.py)
    D --> F[GeoDataFrame]
    E --> F
    F -->|Load: Upsert| G(app/loader.py)
    G -->|Insert/Update| H[(PostGIS DB: iris_staging.water_protection_zones)]

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
Windows 11

Docker Desktop & Docker Compose

PostgreSQL 16 with PostGIS 3.4 (automatically handled by Docker)

Python 3.11+ (if running tests locally)

Git

git clone https://github.com/gideonaggreyfynn/IRIS-WSG-HE.git
cd IRIS-WSG-HE

📊 Data Provenance
Source: Hessisches Landesamt für Naturschutz, Umwelt und Geologie (HLNUG)

Endpoint: https://gds.hessen.de/wfs/hlnug/wasserschutz

Layer: he_wasserschutz_zonen

Transformation: Validated and transformed to EPSG:25832.

Destination: iris_staging.water_protection_zones

⚠️ Assumptions & Limitations
Rate Limiting: The HLNUG WFS service limits requests and may block rapid access. The fixture fallback is provided to ensure reproducible testing without bypassing server restrictions.

Missing Attributes: Where extraction rates or update dates are absent in the source data, they are explicitly stored as NULL.

Staging Only: This module strictly writes to the iris_staging schema and does not interact with production systems (iris_core).

🚀 Run Instructions
Prerequisite: Ensure Docker Desktop is running.

Start the database and run the ingestion pipeline:
docker compose up --build

The pipeline will wait for the database to be healthy, run the init.sql script to create the schema, and execute the ingestion.

Generate the Quality/Error Report:
docker compose run --rm ingest python scripts/quality_report.py

🧪 Automated Testing
The project includes a pytest suite covering schema mapping and geometry repairs.
1. Create and activate a virtual environment:
python -m venv .venv
.venv\Scripts\activate

2. Install development dependencies:
pip install -e ".[dev]"

3. Run the tests:
python -m pytest