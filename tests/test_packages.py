from datasette.app import Datasette
import pytest


@pytest.mark.asyncio
async def test_html():
    datasette = Datasette([], memory=True)
    response = await datasette.client.get("/-/packages")
    assert response.status_code == 200
    assert response.headers["content-type"] == "text/html; charset=utf-8"
    assert "<h1>Installed Packages</h1>" in response.text
    assert "<ul>" in response.text
    # Should contain a link to the datasette package detail page
    assert '<a href="/-/packages/datasette">datasette</a>' in response.text


@pytest.mark.asyncio
async def test_json():
    datasette = Datasette([], memory=True)
    response = await datasette.client.get("/-/packages.json")
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/json; charset=utf-8"
    assert "datasette" in response.json()


@pytest.mark.asyncio
async def test_package_detail():
    datasette = Datasette([], memory=True)
    response = await datasette.client.get("/-/packages/datasette")
    assert response.status_code == 200
    assert response.headers["content-type"] == "text/html; charset=utf-8"
    assert "<h1>datasette</h1>" in response.text
    # Should contain metadata
    assert "Name" in response.text
    assert "Version" in response.text


@pytest.mark.asyncio
async def test_package_detail_not_found():
    datasette = Datasette([], memory=True)
    response = await datasette.client.get("/-/packages/nonexistent-package-xyz")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_package_detail_readme():
    datasette = Datasette([], memory=True)
    # datasette itself should have a README
    response = await datasette.client.get("/-/packages/datasette")
    assert response.status_code == 200
    assert (
        'style="white-space: pre-wrap;"' in response.text
        or "<h2>README</h2>" in response.text
    )


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
