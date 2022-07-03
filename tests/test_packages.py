from datasette.app import Datasette
import pytest


@pytest.mark.asyncio
async def test_html():
    datasette = Datasette([], memory=True)
    response = await datasette.client.get("/-/packages")
    assert response.status_code == 200
    assert response.headers["content-type"] == "text/html; charset=utf-8"
    assert "&#34;datasette&#34;: &#34;" in response.text
    assert "<h1>package.json</h1>" in response.text


@pytest.mark.asyncio
async def test_json():
    datasette = Datasette([], memory=True)
    response = await datasette.client.get("/-/packages.json")
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/json; charset=utf-8"
    assert "datasette" in response.json()


@pytest.mark.asyncio
async def test_graphql():
    datasette = Datasette([], memory=True)
    response = await datasette.client.post(
        "/graphql",
        json={
            "query": """{
                packages {
                    name
                    version
                }
            }"""
        },
    )
    assert response.status_code == 200
    data = response.json()["data"]
    assert "packages" in data
    packages = data["packages"]
    assert isinstance(packages, list)
    assert len(packages) > 0
    first = packages[0]
    assert "name" in first
    assert "version" in first
