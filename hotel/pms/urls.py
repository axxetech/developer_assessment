from django.urls import path

from hotel.pms.view import UpsellProductsView

urlpatterns = [
    path('hotels/<int:hotel_id>/upsell-products/', UpsellProductsView.as_view(), name='retrieve_upsell_products'),
]