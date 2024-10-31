from abc import ABC, abstractmethod
import inspect
import sys

from typing import Optional, Type, TypedDict

from hotel.external_api import (
    get_reservations_for_given_checkin_date,
    get_reservation_details,
    get_guest_details,
    APIError,
)

from hotel.models import Stay, Hotel


class CleanedWebhookPayload(TypedDict):
    hotel_id: int
    data: dict


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

    @abstractmethod
    def stay_has_breakfast(self, stay: Stay) -> Optional[bool]:
        """
        This method is called when we want to know if the stay includes breakfast.
        Notice that the breakfast data is not stored in any of the models, we always want real time data.
        - Return True if the stay includes breakfast, otherwise False. Return None if you don't know.
        """
        raise NotImplementedError


class PMS_Apaleo(PMS):
    @classmethod
    def clean_webhook_payload(cls, payload: str) -> Optional[CleanedWebhookPayload]:
        return None

    def handle_webhook(self, webhook_data: dict) -> bool:
        return False

    def stay_has_breakfast(self, stay: Stay) -> Optional[bool]:
        return None


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
