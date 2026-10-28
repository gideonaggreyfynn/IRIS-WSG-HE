import pytest
from app.schema_mapping import map_zone_code, RestrictionCategory

@pytest.mark.parametrize("raw,expected", [
    ("I", RestrictionCategory.ZONE_I),
    ("2", RestrictionCategory.ZONE_II),
    ("IIIA", RestrictionCategory.ZONE_IIIA),
    (None, RestrictionCategory.UNKNOWN),
    ("garbage", RestrictionCategory.UNKNOWN),
])
def test_zone_mapping(raw, expected):
    assert map_zone_code(raw) == expected