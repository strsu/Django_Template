import graphene
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

from api.v1.model_view_set.models import Product, ProductType


class ProductGraphqlType(DjangoObjectType):
    class Meta:
        model = Product
        fields = "__all__"
        # fields = ("id", "name", "price", "type")


class ProductTypeGraphqlType(DjangoObjectType):
    class Meta:
        model = ProductType
        fields = ("id", "name", "product_set")


class Product_TypeQuery(graphene.ObjectType):
    """
    query {
        allProducts { // 아래 graphene.List가 product 이름이랑 같아야 한다.
            id
            name
            price
            type {
                id
                name
            }
        }
    }
    query {
        categoryByName(name: "옷") {
            id
            name
            productSet {
                id
                name
            }
        }
    }
    """

    all_products = graphene.List(ProductGraphqlType)
    category_by_name = graphene.Field(
        ProductTypeGraphqlType, name=graphene.String(required=True)
    )

    def resolve_all_products(self, info, **kwargs):
        return Product.objects.select_related("type").all()

    def resolve_category_by_name(root, info, name):
        try:
            return ProductType.objects.get(name=name)
        except ProductType.DoesNotExist:
            return None


product_type_schema = graphene.Schema(query=Product_TypeQuery)

########################################################################
########################################################################


class ProductGraphqlNode(DjangoObjectType):
    class Meta:
        model = Product
        # Allow for some more advanced filtering here
        # filter_fields = ["name", "type"]
        interfaces = (graphene.relay.Node,)


class ProductTypeGraphqlNode(DjangoObjectType):
    class Meta:
        model = ProductType
        interfaces = (graphene.relay.Node,)


class Product_NodeQuery(graphene.ObjectType):
    """
    query {
        allProducts { // 아래 graphene.List가 product 이름이랑 같아야 한다.
            id
            name
            price
            type {
                id
                name
            }
        }
    }
    query {
        categoryByName(name: "옷") {
            id
            name
            productSet {
                id
                name
            }
        }
    }
    """

    category = graphene.relay.Node.Field(ProductTypeGraphqlNode)
    all_categories = DjangoFilterConnectionField(ProductTypeGraphqlNode)

    prduct = graphene.relay.Node.Field(ProductGraphqlNode)
    all_products = DjangoFilterConnectionField(ProductGraphqlNode)


# product_node_schema = graphene.Schema(query=Product_NodeQuery)
