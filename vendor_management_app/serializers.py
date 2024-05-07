from rest_framework import serializers
from .models import Vendor, PurchaseOrder,HistoricalPerformance

class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = ['name', 'contact_details', 'address', 'vendor_code']
        read_only_fields = ('on_time_delivery_rate', 'quality_rating_avg', 'average_response_time', 'fulfillment_rate')

class PurchaseOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseOrder
        fields = ['vendor', 'po_number', 'order_date', 'items', 'quantity',  'status']
        read_only_fields = ('issue_date', 'acknowledgment_date', 'quality_rating', 'calculate_quality_rating_avg', 'calculate_average_response_time')

class HistoricalPerformanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistoricalPerformance
        fields = '__all__'