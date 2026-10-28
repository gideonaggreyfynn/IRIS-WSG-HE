import geopandas as gpd
from shapely.validation import make_valid
from app.config import settings
import logging

log = logging.getLogger(__name__)

def validate_geometries(gdf: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    if gdf.empty:
        return gdf

    invalid_mask = ~gdf.geometry.is_valid
    if invalid_mask.any():
        log.warning(f"Repairing {invalid_mask.sum()} invalid geometries.")
        gdf.loc[invalid_mask, "geometry"] = gdf.loc[invalid_mask, "geometry"].apply(make_valid)

    if gdf.crs is None:
        raise ValueError("Source CRS is missing; cannot transform.")
    
    if gdf.crs.to_epsg() != settings.target_srid:
        log.info(f"Transforming CRS from {gdf.crs} to EPSG:{settings.target_srid}")
        gdf = gdf.to_crs(epsg=settings.target_srid)

    return gdf