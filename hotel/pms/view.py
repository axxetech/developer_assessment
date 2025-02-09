import logging

from django.http import JsonResponse
from django.views import View
from hotel.models import Hotel

logger = logging.getLogger(__name__)


class UpsellProductsView(View):

    def get(self, request, hotel_id):
        try:
            hotel = Hotel.objects.get(pk=hotel_id)
        except Hotel.DoesNotExist:
            return JsonResponse({'error': 'Hotel not found'}, status=404)

        try:
            pms_provider = hotel.get_pms()
        except Exception as e:
            logger.error(f"Error retrieving PMS provider for hotel {hotel_id}: {e}")
            return JsonResponse({'error': 'PMS provider error'}, status=500)

        try:
            upsell_products = pms_provider.get_upsell_products()
        except Exception as e:
            logger.error(f"Error retrieving upsell products for hotel {hotel_id}: {e}")
            return JsonResponse({'error': 'Error retrieving upsell products'}, status=500)

        # Serialize each product; we assume each is a Pydantic model with a .dict() method.
        products_data = [product.dict() for product in upsell_products] if upsell_products else []
        return JsonResponse({'upsell_products': products_data}, status=200)
