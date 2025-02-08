import inspect
import json
import logging
import sys
import uuid
from abc import ABC, abstractmethod
from typing import Optional, Type, TypedDict

from hotel.models import Hotel


class CleanedWebhookPayload(TypedDict):
    hotel_id: int
    data: dict


logger = logging.getLogger(__name__)


class PMS(ABC):
    """
    Abstract class for Property Management Systems.
    """

    def __init__(self, hotel: Hotel):
        assert hotel is not None

        self.hotel = hotel

    @property
    def name(self):
        longname = self.__class__.__name__
        return longname[4:]

    @classmethod
    def clean_webhook_payload(cls, payload: str) -> Optional[CleanedWebhookPayload]:
        """
        This method returns a CleanedWebhookPayload object containing a hotel_id from the payload and the data as a dict in the data field
        It should return None if the payload is invalid or the hotel is not found.
        """
        raise NotImplementedError

    @abstractmethod
    def handle_webhook(self, webhook_data: dict) -> bool:
        """
        This method is called when we receive a webhook from the PMS.
        Handle webhook handles the events and updates relevant models in the database.
        Requirements:
            - Now that the PMS has notified you about an update of a reservation, you need to
                get more details of this reservation. For this, you can use the mock API
                call get_reservation_details(reservation_id).
            - Handle the payload for the correct hotel.
            - Update or create a Stay.
            - Update or create Guest details.
        """
        raise NotImplementedError


class PMS_Apaleo(PMS):
    @classmethod
    def clean_webhook_payload(cls, payload: str) -> Optional[CleanedWebhookPayload]:
        if payload is None:
            return None

        try:
            payload_json = json.loads(payload)
        except json.JSONDecodeError:
            return None

        pms_hotel_id: Optional[str] = payload_json.get("HotelId", None)
        try:
            _ = uuid.UUID(pms_hotel_id)
        except ValueError:
            return None

        events = {}
        for event in payload_json.get("Events", []):
            name = event.get("Name", None)
            reservation_id = event["Value"]["ReservationId"]
            if name not in events:
                events[name] = []
            events[name].append(reservation_id)

        try:
            hotel = Hotel.objects.get(pms_hotel_id=pms_hotel_id,
                                      pms=Hotel.PMS.APALEO)
            return CleanedWebhookPayload(hotel_id=hotel.id, data=events)
        except Hotel.DoesNotExist:
            logger.error(f"Hotel with pms_hotel_id {pms_hotel_id} not found.")
        return None


    def handle_webhook(self, webhook_data: dict) -> bool:
        return False


def get_pms(name: str) -> Type[PMS]:
    """
    This function returns the PMS class for the given name.
    This does not return an instance of the class, but the class itself.
    Note, that the name should be the same as the class name without the 'PMS_' prefix.
    """
    fullname = "PMS_" + name.capitalize()
    # find all class names in this module
    # from https://stackoverflow.com/questions/1796180/
    current_module = sys.modules[__name__]
    clsnames = [x[0] for x in inspect.getmembers(current_module, inspect.isclass)]

    # if we have a PMS class for the given name, return an instance of it
    if fullname in clsnames:
        return getattr(current_module, fullname)
    else:
        raise ValueError(f"No PMS class found for {name}")
