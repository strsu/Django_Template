import graphene

from backend.api.v1.model_view_set import schema as graphql_schema


class Query(graphql_schema.ProductQuery, graphene.ObjectType):
    # This class will inherit from multiple Queries
    # as we begin to add more apps to our project
    pass


"""
## settings.py에 GRAPHENE 변수에 등록해야된다.
-> GRAPHENE = {"SCHEMA": "config.schema"}
"""
# schema = graphene.Schema(query=Query)
