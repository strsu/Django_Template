from rest_framework import serializers

from api.v1.model_view_set.models import Product, ProductType


class ProductTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductType
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"


class ProductTypeRawSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=64)

    def create(self, validated_data):
        soccer = ProductType.objects.create(**validated_data)
        return soccer

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.save()
        return instance

    class Meta:
        model = ProductType
        fields = "__all__"


class ProductRawSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=64)
    price = serializers.IntegerField()
    type = ProductTypeRawSerializer(required=False, allow_null=True)
    memo = serializers.CharField(max_length=256)
    demo_1 = serializers.CharField(max_length=64, required=False, allow_null=True)
    demo_2 = serializers.CharField(max_length=64, required=False, allow_null=True)
    demo_3 = serializers.CharField(max_length=64, required=False, allow_null=True)
    demo_4 = serializers.CharField(max_length=64, required=False, allow_null=True)
    demo_5 = serializers.CharField(max_length=64, required=False, allow_null=True)
    demo_6 = serializers.CharField(max_length=64, required=False, allow_null=True)

    def create(self, validated_data):
        product = Product.objects.create(**validated_data)
        return product

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.price = validated_data.get("price", instance.price)
        instance.memo = validated_data.get("memo", instance.memo)
        instance.demo_1 = validated_data.get("demo_1", instance.demo_1)
        instance.demo_2 = validated_data.get("demo_2", instance.demo_2)
        instance.demo_3 = validated_data.get("demo_3", instance.demo_3)
        instance.demo_4 = validated_data.get("demo_4", instance.demo_4)
        instance.demo_5 = validated_data.get("demo_5", instance.demo_5)
        instance.demo_6 = validated_data.get("demo_6", instance.demo_6)

        type = validated_data.get("type")
        if type:
            instance.type = type
        instance.save()
        return instance

    class Meta:
        model = Product
        fields = "__all__"
