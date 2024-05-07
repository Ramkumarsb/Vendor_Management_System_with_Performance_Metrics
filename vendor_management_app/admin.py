from django.contrib import admin
from .models import Vendor, PurchaseOrder, HistoricalPerformance
# Register your models here.


@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    list_display = ('name', 'contact_details', 'address', 'vendor_code', 'on_time_delivery_rate', 'quality_rating_avg', 'average_response_time', 'fulfillment_rate')
    search_fields = ('name', 'vendor_code')

@admin.register(PurchaseOrder)
class PurchaseOrderAdmin(admin.ModelAdmin):
    list_display = ('po_number', 'vendor', 'order_date', 'items', 'quantity', 'status', 'delivery_date', 'quality_rating', 'issue_date', 'acknowledgment_date')
    list_filter = ('vendor', 'status', 'delivery_date')
    search_fields = ('po_number', 'vendor__name')

@admin.register(HistoricalPerformance)
class HistoricalPerformanceAdmin(admin.ModelAdmin):
    list_display = ('vendor', 'date', 'on_time_delivery_rate', 'quality_rating_avg', 'average_response_time', 'fulfillment_rate')
    list_filter = ('vendor', 'date')
