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

    """
    ### Serializer 공부!!!!!

    ## 이렇게 하면 id, plant_id 가 있는 경우엔 update, 없으면 create 하는 방식으로 구별할 수 있다.
    id = serializers.IntegerField(required=False)
    product_id = serializers.IntegerField(required=False, write_only=True)

    name = serializers.CharField(max_length=64, read_only=True) # get에서만 호출된다.
    name = serializers.CharField(max_length=64, write_only=True) # post에서만 호출된다.

    두 개 모두 같은 역할을 한다. list로 받을 수 있다.
    product = ProductSerializer(required=False, allow_null=True, many=True)
    product = serializers.ListField(
        required=False, allow_null=True, child=ProductSerializer()
    )
    """

    def create(self, validated_data):
        return ProductType.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.save()
        return instance

    def to_representation(self, instance):
        """
        to_representation은 retrieve 함수 등 get_serializer(instance).data
        를 호출할 때 실행되어 진다.
        따라서 deserializer후 원하는 값을 넣고싶으면 이곳에서 넣으면 된다.
        혹은 역참조하고 있는 model의 값을 여기서 넣을수도 있다.

        instance : 당연히 이 serializer의 model이다, 즉 ProductType
        """
        ret = super().to_representation(instance)

        product_objs = Product.actives.filter(type=instance)
        product = ProductSerializer(product_objs, many=True)
        ret.update({"inverter": product.data})

        return ret

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
        """
        return Product(**validated_data)
        예제에서는 Product 저장할 때 위처럼 했으나, 실제 저장이 안 된다.
        drf github에서 serializer.save()를 보면 함수에서 obj를 받고, save없이 return을 해준다.
        여기서 문제는 Mixin에서 이 객체를 받아 save()를 호출하는 로직이 없어서 실제론 저장이 안 되는 문제가 발생한다.
        따라서 아래와 같이 create로 return을 해 줘야 한다.
        ...그럼 뭐하러 save()를 호출하는거지?
        """
        return Product.objects.create(**validated_data)

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

        instance.save()  # 아마 이것도 create 처럼 이곳에서 save()를 호출하지 않는다면, 업데이트가 안되는 초유의 사태가 발생할 것이다.
        return instance

    class Meta:
        model = Product
        fields = "__all__"
