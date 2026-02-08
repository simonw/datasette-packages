from datasette import hookimpl, Response
from pathlib import Path
import json
import importlib.metadata


async def packages(request, datasette):
    installed_packages = [
        {"name": d.metadata["Name"], "version": d.version}
        for d in sorted(
            importlib.metadata.distributions(),
            key=lambda d: d.metadata["Name"].lower(),
        )
    ]
    if request.url_vars["format"] == ".json":
        return Response.json({p["name"]: p["version"] for p in installed_packages})
    else:
        return Response.html(
            await datasette.render_template(
                "packages_list.html",
                {"packages": installed_packages},
                request=request,
            )
        )


async def package_detail(request, datasette):
    package_name = request.url_vars["package_name"]
    try:
        dist = importlib.metadata.distribution(package_name)
    except importlib.metadata.PackageNotFoundError:
        return Response.text("Package not found", status=404)

    metadata_items = []
    seen_keys = set()
    for key in dist.metadata.keys():
        if key not in seen_keys:
            seen_keys.add(key)
            values = dist.metadata.get_all(key)
            metadata_items.append((key, values))

    readme = dist.metadata.get_payload()
    if not readme or not readme.strip():
        readme = None

    return Response.html(
        await datasette.render_template(
            "package_detail.html",
            {
                "package_name": dist.metadata["Name"],
                "metadata_items": metadata_items,
                "readme": readme,
            },
            request=request,
        )
    )


@hookimpl
def register_routes():
    return [
        (r"^/-/packages(?P<format>\.json)?$", packages),
        (r"^/-/packages/(?P<package_name>[^/]+)$", package_detail),
    ]


@hookimpl
def extra_template_dirs():
    return [str(Path(__file__).parent / "templates")]


@hookimpl
def graphql_extra_fields():
    import graphene

    class Package(graphene.ObjectType):
        "An installed package"
        name = graphene.String()
        version = graphene.String()

    return [
        (
            "packages",
            graphene.Field(
                graphene.List(Package),
                description="List of installed packages",
                resolver=lambda root, info: [
                    {"name": d.metadata["Name"], "version": d.version}
                    for d in sorted(
                        importlib.metadata.distributions(),
                        key=lambda d: d.metadata["Name"].lower(),
                    )
                ],
            ),
        ),
    ]
