from datasette.app import Datasette
import pytest


@pytest.mark.asyncio
async def test_html():
    datasette = Datasette([], memory=True)
    response = await datasette.client.get("/-/packages")
    assert response.status_code == 200
    assert response.headers["content-type"] == "text/html; charset=utf-8"
    assert "&#34;datasette&#34;: &#34;" in response.text


@pytest.mark.asyncio
async def test_json():
    datasette = Datasette([], memory=True)
    response = await datasette.client.get("/-/packages.json")
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/json; charset=utf-8"
    assert "datasette" in response.json()
