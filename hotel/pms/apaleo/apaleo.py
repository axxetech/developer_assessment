import json
import logging
import uuid
from typing import Optional

from hotel.models import Hotel
from hotel.pms.base import CleanedWebhookPayload, PMSProvider

logger = logging.getLogger(__name__)


class Apaleo(PMSProvider):

    @classmethod
    def clean_webhook_payload(cls, payload: str) \
            -> Optional[CleanedWebhookPayload]:
        if not payload:  # Check for empty or invalid payload early
            logger.error("Payload is missing or empty.")
            return None

        try:
            payload_json = json.loads(payload)
        except json.JSONDecodeError:
            logger.error("Failed to parse payload as JSON.")
            return None

        pms_hotel_id: Optional[str] = payload_json.get("HotelId")
        try:
            if not pms_hotel_id:
                raise ValueError("Invalid pms_hotel_id: None")
            uuid.UUID(pms_hotel_id)  # Validate UUID
        except (ValueError, TypeError) as e:
            logger.error(f"Invalid pms_hotel_id: {pms_hotel_id} - {e}")
            return None

        events = {}
        for event in payload_json.get("Events", []):
            name = event.get("Name")
            reservation_id = event.get("Value", {}).get("ReservationId")
            if not reservation_id:  # Ensure ReservationId exists
                logger.warning(f"Skipping event with missing reservation_id: {event}")
                continue
            if name not in events:
                events[name] = []
            events[name].append(reservation_id)

        try:
            hotel = Hotel.objects.get(pms_hotel_id=pms_hotel_id, pms=Hotel.PMS.APALEO)
            logger.info(f"Hotel found: {hotel.name} (id={hotel.id})")
            return CleanedWebhookPayload(hotel_id=hotel.id, data=events)
        except Hotel.DoesNotExist:
            logger.error(f"Hotel with pms_hotel_id {pms_hotel_id} not found.")
            return None

    def handle_webhook(self, webhook_data: dict) -> bool:
        return False