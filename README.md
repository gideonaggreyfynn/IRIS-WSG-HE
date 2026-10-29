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

##📋 Requirements

*   **Docker Desktop & Docker Compose
*   **PostgreSQL 16 with PostGIS 3.4 (automatically handled by Docker)
*   **Python 3.11+ (if running tests locally)
*   **Git