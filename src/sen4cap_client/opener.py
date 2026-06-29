from typing import Any

import httpx
import pystac
import rioxarray as rio
from cuiman.api.opener import JobResultOpener, JobResultOpenContext
from gavicore.models import Link


class Sen4CAPJobResultsOpener(JobResultOpener):
    async def accept_job_result(self, ctx: JobResultOpenContext) -> bool:
        output_value = ctx.output_value
        if not isinstance(output_value, Link):
            return False

        asset_name = (ctx.options or {}).get("asset_name")
        if not (isinstance(asset_name, str) and bool(asset_name)):
            return False

        stac_url = output_value.href
        return (
            (stac_url.startswith("http://") or stac_url.startswith("https://"))
            and "/collections/" in stac_url
            and "/items/" in stac_url
        )

    async def open_job_result(self, ctx: JobResultOpenContext) -> Any:
        assert isinstance(ctx.output_value, Link)
        assert isinstance(ctx.output_value.href, str)

        # The job output is a link to a STAC item.
        stac_url: str = ctx.output_value.href

        # The desired asset's name
        asset_name: str = (ctx.options or {}).get("asset_name")
        assert isinstance(asset_name, str) and bool(asset_name)

        # The STAC item contains an assets dictionary, giving links to the
        # actual data which was generated. Again, the data item is a URL linking
        # to the actual data – in this case a TIFF file.
        with httpx.Client() as httpx_client:
            response = httpx_client.get(stac_url)
            stac_json = response.json()
            stac_item = pystac.Item.from_dict(stac_json)

        stac_asset = stac_item.assets[asset_name]
        s3_url = stac_asset.extra_fields["alternate"]["s3"]["href"]

        # Now we can use rasterio and xarray to open the output data file
        return rio.open_rasterio(s3_url)
