## Endpoints Directory

All the routes used for the API system is defined and listed in this directory

To add new routes to the API system:
1. Create a file for that api router. Define and implement all the endpoints in that route
2. Add the Tag for the new Router to the `TAGS_METADATA` list in the `__init__.py` file in this directory.
3. The name for new route can be `<name>_router` and the name for the corresponding tag should be `<name>` with first letter Capitalised. Example, router name is `user_router` while the tag is `User` 
4. Make sure the format of your entry is `{ <tag_name>: <tag description> } `. This tag will help to add metadata to the openapi tags. The value of `<tag_name>` is mapped against `TAGS_METADATA` to fetch the description of the `<tag_name>`
