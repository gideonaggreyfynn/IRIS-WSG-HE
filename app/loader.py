from sqlalchemy import text
from sqlalchemy.engine import Engine
from app.config import settings

UPSERT_SQL = """
INSERT INTO {schema}.{table}
    (source_zone_id, state_code, zone_code, restriction_category,
     extraction_rate, geometry, source_url, source_updated_at, ingested_at)
VALUES
    (:source_zone_id, :state_code, :zone_code, :restriction_category,
     :extraction_rate, ST_GeomFromText(:geometry_wkt, :srid),
     :source_url, :source_updated_at, NOW())
ON CONFLICT (source_zone_id, state_code)
DO UPDATE SET
    zone_code = EXCLUDED.zone_code,
    restriction_category = EXCLUDED.restriction_category,
    extraction_rate = EXCLUDED.extraction_rate,
    geometry = EXCLUDED.geometry,
    source_url = EXCLUDED.source_url,
    source_updated_at = EXCLUDED.source_updated_at,
    ingested_at = NOW()
;
"""

def load_zones(engine: Engine, records: list[dict]):
    sql = UPSERT_SQL.format(
        schema=settings.staging_schema,
        table=settings.staging_table,
    )
    with engine.begin() as conn:
        conn.execute(text(sql), records)