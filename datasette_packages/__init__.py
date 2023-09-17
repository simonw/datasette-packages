from datasette import hookimpl, Response
import json
import sqlite_utils
import pkg_resources
import importlib.metadata


@hookimpl
def startup(datasette):
    packages_db = datasette.add_memory_database("packages")

    def populate(conn):
        db = sqlite_utils.Database(conn)

        def packages():
            for distro in importlib.metadata.distributions():
                d = {
                    "name": distro.metadata["Name"],
                    "version": distro.version,
                }
                multi_keys = {k.lower() for k in distro.metadata.multiple_use_keys}
                for key in distro.metadata.keys():
                    if key.lower() in multi_keys:
                        d[key.lower()] = distro.metadata.get_all(key)
                    else:
                        d[key.lower()] = distro.metadata[key]
                yield d

        with conn:
            db["packages"].insert_all(packages(), pk="name", replace=True)

    async def inner():
        await packages_db.execute_write_fn(populate)

    return inner


async def packages(request, datasette):
    installed_packages = {
        d.project_name: d.version
        for d in sorted(pkg_resources.working_set, key=lambda d: d.project_name.lower())
    }
    if request.url_vars["format"] == ".json":
        return Response.json(installed_packages)
    else:
        return Response.html(
            await datasette.render_template(
                "show_json.html",
                {
                    "filename": "package.json",
                    "data_json": json.dumps(installed_packages, indent=4),
                },
                request=request,
            )
        )


@hookimpl
def register_routes():
    return [(r"^/-/packages(?P<format>\.json)?$", packages)]


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
                    {"name": d.project_name, "version": d.version}
                    for d in sorted(
                        pkg_resources.working_set, key=lambda d: d.project_name.lower()
                    )
                ],
            ),
        ),
    ]
