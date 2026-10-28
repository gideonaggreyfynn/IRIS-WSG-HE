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
    A[HLNUG WFS Server\nor Local GML Fixture] -->|Extract: Raw GML| B(app/wfs_client.py)
    B -->|Parse XML| C(main.py)
    C -->|Transform: Map Zones| D(app/schema_mapping.py)
    C -->|Transform: Repair & Reproject| E(app/validation.py)
    D --> F{GeoDataFrame}
    E --> F
    F -->|Load: Upsert| G(app/loader.py)
    G -->|Insert/Update| H[(PostGIS DB:\niris_staging.water_protection_zones)]