#!/usr/bin/env python3
import logging
import io
import geopandas as gpd

from app.config import settings
from app.wfs_client import WFSClient
from app.schema_mapping import map_zone_code
from app.validation import validate_geometries
from app.loader import load_zones
from app.database import get_engine

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

def main():
    log.info("Starting Hesse WSG ingestion.")
    client = WFSClient()
    
    gml_bytes = client.get_features()
    
    log.info("Parsing GML features into GeoDataFrame...")
    gdf = gpd.read_file(io.BytesIO(gml_bytes), driver="GML")
    
    if gdf.empty:
        log.error("No features parsed.")
        return

    if 'zone' in gdf.columns:
        gdf['restriction_category'] = gdf['zone'].apply(lambda x: map_zone_code(x).value)
    else:
        gdf['restriction_category'] = "Unknown"

    gdf = gdf.rename(columns={'zone': 'zone_code'})
    gdf['source_zone_id'] = gdf['id'] if 'id' in gdf.columns else "unknown_id"
    gdf['state_code'] = "HE"
    gdf['source_url'] = settings.wfs_url
    
    for col in ['extraction_rate', 'source_updated_at']:
        if col not in gdf.columns:
            gdf[col] = None

    gdf = validate_geometries(gdf)

    records = gdf.to_dict("records")
    for rec in records:
        rec["geometry_wkt"] = rec.pop("geometry").wkt
        rec["srid"] = settings.target_srid

    engine = get_engine()
    load_zones(engine, records)
    log.info(f"Ingestion complete: {len(records)} records upserted.")

if __name__ == "__main__":
    main()