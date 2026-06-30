import pytest
import xarray as xr
from cuiman.api.opener import JobResultOpenContext, JobResultOpenerRegistry
from cuiman.api.opener.opener import open_job_result
from gavicore.models import JobResults

from sen4cap_client.api import Sen4CAPConfig
from sen4cap_client.opener import Sen4CAPJobResultsOpener

# Happy-path job results
job_results_example = JobResults(
    **{
        "db96d3e8-0243-48dc-ac9a-6470d2c39eb8": {
            "type": "application/json",
            "href": "http://sen4x.tao.c-s.ro:8082/collections/L3B_NDVI/items/S2AGRI_L3BNDVI_PRD_S23_20260629T093945_A20240607T102559_T32UNE",
        }
    }
)

# A typical STAC item
stac_item_example = {
    "type": "Feature",
    "stac_version": "1.1.0",
    "stac_extensions": [],
    "id": "S2AGRI_L3BNDVI_PRD_S23_20260629T093945_A20240607T102559_T32UNE",
    "geometry": {
        "type": "Polygon",
        "coordinates": [
            [
                [53.349950513, 9.653786526],
                [53.343764266, 10.379812188],
                [53.74992999, 10.393088385],
                [53.756208125, 9.660079005],
                [53.349950513, 9.653786526],
            ]
        ],
    },
    "bbox": [53.343764266, 9.653786526, 53.756208125, 10.393088385],
    "properties": {"datetime": "2024-06-07T10:25:59Z"},
    "links": [
        {
            "rel": "collection",
            "href": "http://sen4x.tao.c-s.ro:8082/collections/L3B_NDVI",
            "type": "application/json",
        },
        {
            "rel": "parent",
            "href": "http://sen4x.tao.c-s.ro:8082/collections/L3B_NDVI",
            "type": "application/json",
        },
        {
            "rel": "root",
            "href": "http://sen4x.tao.c-s.ro:8082/",
            "type": "application/json",
            "title": "stac-fastapi",
        },
        {
            "rel": "self",
            "href": "http://sen4x.tao.c-s.ro:8082/collections/L3B_NDVI/items/S2AGRI_L3BNDVI_PRD_S23_20260629T093945_A20240607T102559_T32UNE",
            "type": "application/geo+json",
        },
    ],
    "assets": {
        "SNDVI": {
            "href": "/SEN4CAP_L3B/site_12/l3b_ndvi/S2AGRI_L3BNDVI_PRD_S23_20260629T093945_A20240607T102559_T32UNE/TILES/S2AGRI_L3BNDVI_A20240607T102559_T32UNE/IMG_DATA/S2AGRI_L3BNDVI_SNDVI_A20240607T102559_T32UNE.TIF",
            "type": "image/tiff",
            "alternate": {
                "s3": {
                    "href": "http://s3.waw4-1.cloudferro.com/SEN4CAP_L3B/site_12/l3b_ndvi/S2AGRI_L3BNDVI_PRD_S23_20260629T093945_A20240607T102559_T32UNE/TILES/S2AGRI_L3BNDVI_A20240607T102559_T32UNE/IMG_DATA/S2AGRI_L3BNDVI_SNDVI_A20240607T102559_T32UNE.TIF"
                }
            },
            "roles": ["data"],
        },
        "metadata": {
            "href": "/SEN4CAP_L3B/site_12/l3b_ndvi/S2AGRI_L3BNDVI_PRD_S23_20260629T093945_A20240607T102559_T32UNE/S2AGRI_L3BNDVI_MTD_A20240607T102559.xml",
            "type": "application/xml",
            "title": "Product manifest",
            "alternate": {
                "s3": {
                    "href": "http://s3.waw4-1.cloudferro.com/SEN4CAP_L3B/site_12/l3b_ndvi/S2AGRI_L3BNDVI_PRD_S23_20260629T093945_A20240607T102559_T32UNE/S2AGRI_L3BNDVI_MTD_A20240607T102559.xml"
                }
            },
            "roles": ["metadata"],
        },
        "MMONODFLG": {
            "href": "/SEN4CAP_L3B/site_12/l3b_ndvi/S2AGRI_L3BNDVI_PRD_S23_20260629T093945_A20240607T102559_T32UNE/TILES/S2AGRI_L3BNDVI_A20240607T102559_T32UNE/QI_DATA/S2AGRI_L3BNDVI_MMONODFLG_A20240607T102559_T32UNE.TIF",
            "type": "image/tiff",
            "alternate": {
                "s3": {
                    "href": "http://s3.waw4-1.cloudferro.com/SEN4CAP_L3B/site_12/l3b_ndvi/S2AGRI_L3BNDVI_PRD_S23_20260629T093945_A20240607T102559_T32UNE/TILES/S2AGRI_L3BNDVI_A20240607T102559_T32UNE/QI_DATA/S2AGRI_L3BNDVI_MMONODFLG_A20240607T102559_T32UNE.TIF"
                }
            },
            "roles": ["data"],
        },
        "thumbnail": {
            "href": "/SEN4CAP_L3B/site_12/l3b_ndvi/S2AGRI_L3BNDVI_PRD_S23_20260629T093945_A20240607T102559_T32UNE/TILES/S2AGRI_L3BNDVI_A20240607T102559_T32UNE/S2AGRI_L3BNDVI_PVI_A20240607T102559_T32UNE.jpg",
            "type": "image/jpeg",
            "roles": ["thumbnail"],
        },
    },
    "collection": "L3B_NDVI",
}


def mock_opener_io(monkeypatch):
    expected_data = xr.DataArray([1, 2, 3], dims=("x",), name="SNDVI")
    opened_urls = []
    fetched_urls = []

    class MockResponse:
        def json(self):
            return stac_item_example

    class MockHttpxClient:
        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc_val, exc_tb):
            return None

        def get(self, url):
            fetched_urls.append(url)
            return MockResponse()

    def open_rasterio(url):
        opened_urls.append(url)
        return expected_data

    monkeypatch.setattr("sen4cap_client.opener.httpx.Client", MockHttpxClient)
    monkeypatch.setattr("sen4cap_client.opener.rio.open_rasterio", open_rasterio)
    return expected_data, fetched_urls, opened_urls


def expected_stac_url():
    return next(iter(job_results_example.root.values())).href


def expected_s3_url(asset_name):
    return stac_item_example["assets"][asset_name]["alternate"]["s3"]["href"]


@pytest.mark.asyncio
async def test_job_results_opener_accept_job_result():
    opener = Sen4CAPJobResultsOpener()
    config = Sen4CAPConfig(auth_type="none")

    # empty job results -> fail
    ctx = JobResultOpenContext(
        config, "632", JobResults(), options=dict(asset_name="SNDVI")
    )
    assert await opener.accept_job_result(ctx) is False

    # invalid job results -> fail
    ctx = JobResultOpenContext(
        config, "632", JobResults(**{"x": 137}), options=dict(asset_name="SNDVI")
    )
    assert await opener.accept_job_result(ctx) is False

    # missing asset_name -> fail
    ctx = JobResultOpenContext(config, "632", job_results_example)
    assert await opener.accept_job_result(ctx) is False

    # all good -> accept
    ctx = JobResultOpenContext(
        config, "632", job_results_example, options=dict(asset_name="SNDVI")
    )
    assert await opener.accept_job_result(ctx) is True


@pytest.mark.asyncio
async def test_job_results_opener_open_job_result(monkeypatch):
    opener = Sen4CAPJobResultsOpener()
    config = Sen4CAPConfig(auth_type="none")

    expected_data, fetched_urls, opened_urls = mock_opener_io(monkeypatch)

    ctx = JobResultOpenContext(
        config, "632", job_results_example, options=dict(asset_name="SNDVI")
    )
    data = await opener.open_job_result(ctx)

    assert isinstance(data, xr.DataArray)
    assert data is expected_data
    assert fetched_urls == [expected_stac_url()]
    assert opened_urls == [expected_s3_url("SNDVI")]


@pytest.mark.asyncio
async def test_job_results_opener_in_action(monkeypatch):
    registry = JobResultOpenerRegistry.create_default()
    registry.register(Sen4CAPJobResultsOpener)
    config = Sen4CAPConfig(auth_type="none")
    expected_data, fetched_urls, opened_urls = mock_opener_io(monkeypatch)

    ctx = JobResultOpenContext(
        config, "632", job_results_example, options=dict(asset_name="SNDVI")
    )
    data = await open_job_result(ctx, *registry.opener_types)

    assert isinstance(data, xr.DataArray)
    assert data is expected_data
    assert fetched_urls == [expected_stac_url()]
    assert opened_urls == [expected_s3_url("SNDVI")]
