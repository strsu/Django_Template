from rest_framework import serializers
from blog.models import Blog

from datetime import datetime


class BlogSerializer(serializers.ModelSerializer):
    """
    The ModelSerializer class is the same as a regular Serializer class, except that:

        It will automatically generate a set of fields for you, based on the model.
        It will automatically generate validators for the serializer, such as unique_together validators.
        It includes simple default implementations of .create() and .update().
    """

    class Meta:
        """
        확실하진 않지만!
        is_valid에서 fields에 있는 column을 검사하는 것 같다
        user는 null=True라서 상관이 없는거고
        time은 null=False라서 fields에 time을 넣으면 is_valid가 False를 준다
            -> date를 안 넘길시!
        """

        model = Blog
        fields = ["user", "content", "tags"]
        # fields = '__all__'
        # exclude = ['users']
        # read_only_fields = ['account_name']
