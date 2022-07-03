from datasette import hookimpl, Response
import json
import pkg_resources


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
