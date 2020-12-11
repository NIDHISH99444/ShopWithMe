from django.contrib import admin
from .models import Tshirt,Brand,Cart,Order,OrderItem,Payment, Color,Occasion,Sleeve,NeckType,IdealFor,SizeVariant
# Register your models here.

class SizeVariantConfiguration(admin.TabularInline):
    model=SizeVariant

class TshirtConfiguration(admin.ModelAdmin):
    inlines=[ SizeVariantConfiguration ]
    list_display=['name','slug']
  

admin.site.register(Tshirt, TshirtConfiguration)
admin.site.register(Brand)
admin.site.register(Color)
admin.site.register(NeckType)
admin.site.register(Sleeve)
admin.site.register(Occasion)
admin.site.register(IdealFor)
admin.site.register(Cart)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Payment)





