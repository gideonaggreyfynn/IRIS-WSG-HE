import logging
from pathlib import Path
from owslib.wfs import WebFeatureService
from tenacity import retry, stop_after_attempt, wait_exponential
from app.config import settings

log = logging.getLogger(__name__)

class WFSClient:
    def __init__(self):
        self.fixture_path = Path(__file__).parent.parent / "fixtures" / "wfs_features_sample.gml"

    def get_features(self) -> bytes:
        if settings.wfs_use_fixture:
            log.info("Using fixture (live WFS disabled).")
            return self._read_fixture()

        try:
            return self._fetch_live()
        except Exception as exc:
            log.warning("Live WFS failed after retries (%s). Falling back to fixture.", exc)
            return self._read_fixture()

    def _read_fixture(self) -> bytes:
        if not self.fixture_path.exists():
            raise FileNotFoundError(f"Fixture not found at {self.fixture_path}")
        return self.fixture_path.read_bytes()

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=2, min=2, max=30))
    def _fetch_live(self) -> bytes:
        wfs = WebFeatureService(url=settings.wfs_url, version="2.0.0")
        if settings.wfs_layer not in wfs.contents:
            raise ValueError(f"Layer {settings.wfs_layer} not found in WFS capabilities.")

        response = wfs.getfeature(
            typename=settings.wfs_layer,
            maxfeatures=settings.wfs_page_size,
            outputFormat="application/gml+xml; version=3.2",
        )
        return response.read()