from rest_framework import serializers
from api.v1.file.models import File

from datetime import datetime


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ["user", "content", "tags"]
        # fields = '__all__'
        # exclude = ['users']
        # read_only_fields = ['account_name']
