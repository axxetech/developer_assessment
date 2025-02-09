from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import logging

from django.http import HttpResponse
from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from hotel.models import Hotel  # Adjust as needed
from hotel.pms.base import get_pms

logger = logging.getLogger(__name__)


@csrf_exempt
@require_POST
def webhook(request, pms_name):
    """
    Assume a webhook call from the PMS with a status update for a reservation.
    The webhook call is a POST request to the url: /webhook/<pms_name>/
    The body of the request should always be a valid JSON string and contain the needed information to perform an update.
    """

    pms_cls = get_pms(pms_name)

    cleaned_webhook_payload = pms_cls.clean_webhook_payload(request.body)
    if not cleaned_webhook_payload:
        return HttpResponse(status=400)
    hotel = Hotel.objects.get(id=cleaned_webhook_payload["hotel_id"])
    pms = hotel.get_pms()
    success = pms.handle_webhook(cleaned_webhook_payload)
    if not success:
        return HttpResponse(status=400)
    else:
        return HttpResponse("Thanks for the update.")


class HotelsListView(View):
    def get(self, request):
        try:
            hotels = Hotel.objects.all()
            hotels_data = []
            for hotel in hotels:
                hotels_data.append({
                    'id': hotel.id,
                    'name': hotel.name,
                    'city': hotel.city,
                    'pms': hotel.get_pms().name,
                })
            return JsonResponse({'hotels': hotels_data})
        except Exception as e:
            logger.error(f"Error retrieving hotels: {e}")
            return JsonResponse({'error': 'Error retrieving hotels'}, status=500)


def upsell_selector(request):
    return render(request, 'hotel/upsell_selector.html')