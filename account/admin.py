from django.contrib import admin

# Register your models here.
from .models import *

class OrderAdmin(admin.ModelAdmin):
    list_display = ('customer', 'product', 'status')

admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Tag)
admin.site.register(Order, OrderAdmin)

