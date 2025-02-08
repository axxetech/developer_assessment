from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.http import HttpResponse

from hotel import pms_systems

from hotel.models import Hotel


@csrf_exempt
@require_POST
def webhook(request, pms_name):
    """
    Assume a webhook call from the PMS with a status update for a reservation.
    The webhook call is a POST request to the url: /webhook/<pms_name>/
    The body of the request should always be a valid JSON string and contain the needed information to perform an update.
    """

    pms_cls = pms_systems.get_pms(pms_name)

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
