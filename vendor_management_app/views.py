from django.db.models import Avg, F
from django.shortcuts import render
from rest_framework import generics, status
from .models import Vendor, PurchaseOrder, HistoricalPerformance
from .serializers import VendorSerializer, PurchaseOrderSerializer, HistoricalPerformanceSerializer
from datetime import timezone
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
# Create your views here.



class VendorListCreateView(generics.ListCreateAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save()

    def perform_update(self, serializer):
        serializer.save()

    def get_queryset(self):
        queryset = Vendor.objects.all()
        for vendor in queryset:
            vendor.on_time_delivery_rate = vendor.purchaseorder_set.filter(status='completed', delivery_date__lte=F(
                'delivery_date')).count() / vendor.purchaseorder_set.filter(
                status='completed').count() * 100 if vendor.purchaseorder_set.filter(
                status='completed').count() > 0 else 0.0
            vendor.quality_rating_avg = \
            vendor.purchaseorder_set.filter(status='completed', quality_rating__isnull=False).aggregate(
                Avg('quality_rating'))['quality_rating__avg'] if vendor.purchaseorder_set.filter(status='completed',
                                                                                                 quality_rating__isnull=False).count() > 0 else 0.0
            vendor.fulfillment_rate = vendor.purchaseorder_set.filter(status='completed', issue_date__lte=F(
                'acknowledgment_date')).count() / vendor.purchaseorder_set.count() * 100 if vendor.purchaseorder_set.count() > 0 else 0.0
        return queryset

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)



class VendorRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]


class PurchaseOrderListCreateView(generics.ListCreateAPIView):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer

    def perform_create(self, serializer):
        serializer.save()
        if serializer.validated_data['status'] == 'completed':
            serializer.instance.vendor.quality_rating_avg = serializer.instance.calculate_quality_rating_avg()
            serializer.instance.vendor.save()

    def perform_update(self, serializer):
        serializer.save()
        if 'status' in serializer.validated_data and serializer.validated_data['status'] == 'completed':
            serializer.instance.vendor.quality_rating_avg = serializer.instance.calculate_quality_rating_avg()
            serializer.instance.vendor.save()

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class PurchaseOrderRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]


class HistoricalPerformanceListCreateView(generics.ListCreateAPIView):
    queryset = HistoricalPerformance.objects.all()
    serializer_class = HistoricalPerformanceSerializer


class AcknowledgePurchaseOrderView(generics.UpdateAPIView):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer
    http_method_names = ['patch']

    def perform_update(self, serializer):
        serializer.save(acknowledgment_date=timezone.now())
        serializer.instance.vendor.average_response_time = serializer.instance.calculate_average_response_time()
        serializer.instance.vendor.save()


class VendorPerformanceView(generics.RetrieveAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    lookup_url_kwarg = 'vendor_id'
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]