from django.contrib import admin

from .models import Places, Descriptions, enAddress, hkAddress, Review

admin.site.register(Places)
admin.site.register(Descriptions)
admin.site.register(enAddress)
admin.site.register(hkAddress)
admin.site.register(Review)