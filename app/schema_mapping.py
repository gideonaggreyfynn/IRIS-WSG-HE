from enum import Enum

class RestrictionCategory(str, Enum):
    ZONE_I = "Zone I"
    ZONE_II = "Zone II"
    ZONE_III = "Zone III"
    ZONE_IIIA = "Zone IIIA"
    ZONE_IIIB = "Zone IIIB"
    UNKNOWN = "Unknown"

ZONE_CODE_MAP = {
    "I": RestrictionCategory.ZONE_I,
    "1": RestrictionCategory.ZONE_I,
    "II": RestrictionCategory.ZONE_II,
    "2": RestrictionCategory.ZONE_II,
    "2o": RestrictionCategory.ZONE_II, 
    "III": RestrictionCategory.ZONE_III,
    "3": RestrictionCategory.ZONE_III,
    "IIIA": RestrictionCategory.ZONE_IIIA,
    "IIIB": RestrictionCategory.ZONE_IIIB,
}

def map_zone_code(raw_code: str | None) -> RestrictionCategory:
    if raw_code is None:
        return RestrictionCategory.UNKNOWN
    code = str(raw_code).strip().upper()
    return ZONE_CODE_MAP.get(code, RestrictionCategory.UNKNOWN)