import geopandas as gpd
from shapely.geometry import Polygon
from app.validation import validate_geometries

def test_invalid_geometry_is_repaired():
    bowtie = Polygon([(500000,5500000), (501000,5501000), (501000,5500000), (500000,5501000), (500000,5500000)])
    gdf = gpd.GeoDataFrame({"id": [1]}, geometry=[bowtie], crs="EPSG:25832")
    out = validate_geometries(gdf)
    assert out.geometry.is_valid.all()