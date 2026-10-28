&#x20;🗺️ IRIS WSG HE - Hesse Groundwater Protection Zones Ingestion



&#x20;📖 Overview

This repository contains a robust ETL (Extract, Transform, Load) pipeline designed to ingest Hesse groundwater protection zones from the HLNUG OGC WFS service into an isolated PostGIS staging database.



Built to support site-permitting and groundwater restriction screening, this module ensures data traceability, spatial accuracy, and idempotent loading, providing a reliable foundation for environmental geospatial analysis.



&#x20;✨ Key Features

&#x20; Resilient Data Acquisition: Implements OGC WFS paging (handling the 4,000-record limit) and includes an automated fallback to a local fixture (`wfs\\\_features\\\_sample.gml`) if the live service rate-limits (HTTP 429) or is unavailable.

&#x20; Strict Classification Mapping: Official zone codes (e.g., "I", "II", "IIIA") are mapped using a strict, traceable dictionary—no fragile substring heuristics.

&#x20; Geospatial Integrity: Automatically detects and repairs invalid multipart polygons (e.g., bowties) using `shapely.make\\\_valid` and transforms geometries to `EPSG:25832`.

&#x20; Idempotent Database Loading: Utilizes PostgreSQL's `ON CONFLICT DO UPDATE` to ensure that running the pipeline multiple times updates existing records rather than creating duplicates.

&#x20; Quality Reporting: Includes a dedicated script to generate a JSON report detailing loaded features, missing attributes, and coverage limitations.



&#x20;🏗️ System Architecture

The pipeline operates through the following flow:

1\. Extract: `app/wfs\\\_client.py` connects to the HLNUG WFS service (or reads the local fixture) and retrieves raw GML data.

2\. Transform: `main.py` parses the GML into a Geodata Frame. `app/schema\\\_mapping.py` applies strict zone classifications, while `app/validation.py` repairs geometries and transforms the CRS to EPSG:25832.

3\. Load: `app/loader.py` executes an upsert query to insert the validated records into the `iris\\\_staging.water\\\_protection\\\_zones` PostGIS table.



&#x20;📋 Requirements

&#x20; Operating System: Developed and tested on Windows 11 (via Command Prompt/PowerShell).

&#x20; Containerization: Docker Desktop (with Docker Compose).

&#x20; Local Testing: Python 3.11+ (if running `pytest` outside of Docker).



&#x20;📥 Clone the Repository

To get started with this project locally, clone the repository and navigate into the directory:



```bash

git clone https://github.com/YourUsername/IRIS-WSG-HE.git

cd IRIS-WSG-HE




📊 Data Provenance

Source: Hessisches Landesamt für Naturschutz, Umwelt und Geologie (HLNUG)



Endpoint: https://gds.hessen.de/wfs/hlnug/wasserschutz



Layer: he\_wasserschutz\_zonen



Transformation: Validated and transformed to EPSG:25832.



Destination: iris\_staging.water\_protection\_zones



⚠️ Assumptions \& Limitations

Rate Limiting: The HLNUG WFS service limits requests and may block rapid access. The fixture fallback is provided to ensure reproducible testing without bypassing server restrictions.



Missing Attributes: Where extraction rates or update dates are absent in the source data, they are explicitly stored as NULL rather than being inferred.



Staging Only: This module strictly writes to the iris\_staging schema and does not interact with production systems (iris\_core).



\# 🗺️ IRIS WSG HE – Hesse Groundwater Protection Zones Ingestion



!\[Python](https://img.shields.io/badge/Python-3.11+-blue.svg)

!\[Docker](https://img.shields.io/badge/Docker-Compose-2496ED.svg)

!\[PostGIS](https://img.shields.io/badge/Database-PostGIS-336791.svg)

!\[License](https://img.shields.io/badge/License-MIT-green.svg)



\## 📖 Overview



This repository contains a robust, production-ready \*\*ETL (Extract, Transform, Load) pipeline\*\* designed to ingest Hesse groundwater protection zones from the HLNUG OGC WFS service into an isolated PostGIS staging database. 



Built to support site-permitting and groundwater restriction screening, this module ensures \*\*data traceability\*\*, \*\*spatial accuracy\*\*, and \*\*idempotent loading\*\*, providing a reliable foundation for environmental geospatial analysis.



\---



\## 📑 Table of Contents

\- \[✨ Key Features](#-key-features)

\- \[🏗️ System Architecture](#️-system-architecture)

\- \[📋 Requirements](#-requirements)

\- \[🚀 Getting Started](#-getting-started)

\- \[📊 Quality Reporting](#-quality-reporting)



\---



\## ✨ Key Features



\* \*\*🔄 Resilient Data Acquisition:\*\* Implements OGC WFS paging to gracefully handle the 4,000-record limit. Includes an automated fallback to a local fixture (`wfs\_features\_sample.gml`) if the live service rate-limits (HTTP 429) or becomes unavailable.

\* \*\*📏 Strict Classification Mapping:\*\* Official zone codes (e.g., `"I"`, `"II"`, `"IIIA"`) are mapped using a strict, traceable dictionary—eliminating fragile substring heuristics.

\* \*\*🌍 Geospatial Integrity:\*\* Automatically detects and repairs invalid multipart polygons (e.g., bowties) using `shapely.make\_valid` and standardizes all geometries to `EPSG:25832`.

\* \*\*🔒 Idempotent Database Loading:\*\* Utilizes PostgreSQL's `ON CONFLICT DO UPDATE` (upsert) to ensure that running the pipeline multiple times safely updates existing records rather than creating duplicates.

\* \*\*📈 Quality Reporting:\*\* Includes a dedicated script to generate a comprehensive JSON report detailing loaded features, missing attributes, and coverage limitations.



\---



\## 🏗️ System Architecture



The pipeline operates through a clean, modular three-step flow:



1\. \*\*Extract:\*\* `app/wfs\_client.py` connects to the HLNUG WFS service (or reads the local fixture) and retrieves raw GML data.

2\. \*\*Transform:\*\* 

&#x20;  - `main.py` orchestrates the parsing of GML into a GeoDataFrame.

&#x20;  - `app/schema\_mapping.py` applies strict zone classifications.

&#x20;  - `app/validation.py` repairs geometries and transforms the Coordinate Reference System (CRS) to `EPSG:25832`.

3\. \*\*Load:\*\* `app/loader.py` executes an optimized upsert query to insert the validated records into the `iris\_staging.water\_protection\_zones` PostGIS table.



\---



\## 📋 Requirements



\* \*\*Operating System:\*\* Developed and tested on \*\*Windows 11\*\* (via Command Prompt / PowerShell).

\* \*\*Containerization:\*\* \[Docker Desktop](https://www.docker.com/products/docker-desktop/) (with Docker Compose enabled).

\* \*\*Local Testing:\*\* Python 3.11+ (required if running `pytest` or scripts outside of the Docker environment).



\---



\## 🚀 Getting Started



To get started with this project locally, clone the repository and navigate into the directory:



```bash

git clone https://github.com/YourUsername/IRIS-WSG-HE.git

cd IRIS-WSG-HE

