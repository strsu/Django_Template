from django import forms
from django.contrib import admin

from api.common.admin import BaseAdmin

from .models import Goods


class GoodsAdmin(BaseAdmin):
    list_display = ("owner", "title", "content", "image")
    # list_display_links =


admin.site.register(Goods, GoodsAdmin)
