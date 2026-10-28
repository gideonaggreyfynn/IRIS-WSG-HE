# 🗺️ IRIS WSG HE - Hesse Groundwater Protection Zones Ingestion

## 📖 Overview
This repository contains a robust ETL (Extract, Transform, Load) pipeline designed to ingest Hesse groundwater protection zones from the HLNUG OGC WFS service into an isolated PostGIS staging database. 

Built to support site-permitting and groundwater restriction screening, this module ensures data traceability, spatial accuracy, and idempotent loading, providing a reliable foundation for environmental geospatial analysis.

## ✨ Key Features
*   **Resilient Data Acquisition:** Implements OGC WFS paging (handling the 4,000-record limit) and includes an automated fallback to a local fixture (`wfs_features_sample.gml`) if the live service rate-limits (HTTP 429) or is unavailable.
*   **Strict Classification Mapping:** Official zone codes (e.g., "I", "II", "IIIA") are mapped using a strict, traceable dictionary—no fragile substring heuristics.
*   **Geospatial Integrity:** Automatically detects and repairs invalid multipart polygons (e.g., bowties) using `shapely.make_valid` and transforms geometries to `EPSG:25832`.
*   **Idempotent Database Loading:** Utilizes PostgreSQL's `ON CONFLICT DO UPDATE` to ensure that running the pipeline multiple times updates existing records rather than creating duplicates.
*   **Quality Reporting:** Includes a dedicated script to generate a JSON report detailing loaded features, missing attributes, and coverage limitations.

## 🏗️ System Architecture
The pipeline operates through the following flow:
1.  **Extract:** `app/wfs_client.py` connects to the HLNUG WFS service (or reads the local fixture) and retrieves raw GML data.
2.  **Transform:** `main.py` parses the GML into a GeoDataFrame. `app/schema_mapping.py` applies strict zone classifications, while `app/validation.py` repairs geometries and transforms the CRS to EPSG:25832.
3.  **Load:** `app/loader.py` executes an upsert query to insert the validated records into the `iris_staging.water_protection_zones` PostGIS table.

## 📋 Requirements
*   **Operating System:** Developed and tested on **Windows 11** (via Command Prompt/PowerShell).
*   **Containerization:** Docker Desktop (with Docker Compose).
*   **Local Testing:** Python 3.11+ (if running `pytest` outside of Docker).

## 📥 Clone the Repository
To get started with this project locally, clone the repository and navigate into the directory:

```bash
git clone https://github.com/gideonaggreyfynn/IRIS-WSG-HE
cd IRIS-WSG-HE

Data Provenance
Source: Hessisches Landesamt für Naturschutz, Umwelt und Geologie (HLNUG)
Endpoint: https://gds.hessen.de/wfs/hlnug/wasserschutz
Layer: he_wasserschutz_zonen
Transformation: Validated and transformed to EPSG:25832.
Destination: iris_staging.water_protection_zones

🚀 Run Instructions
Prerequisite: Ensure Docker Desktop is running.
Start the database and run the ingestion pipeline:
bash
docker compose up --build
The pipeline will wait for the database to be healthy, run the init.sql script to create the schema, and execute the ingestion.
