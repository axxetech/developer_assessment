import importlib
import inspect
import logging
import pkgutil
from abc import ABC, abstractmethod
from typing import Optional, Type, TypedDict

from hotel.models import Hotel


class CleanedWebhookPayload(TypedDict):
    hotel_id: int
    data: dict


logger = logging.getLogger(__name__)


class PMSProvider(ABC):
    """
    Abstract class for Property Management Systems.
    """

    def __init__(self, hotel: Hotel):
        assert hotel is not None

        self.hotel = hotel

    @property
    def name(self):
        return self.__class__.__name__

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
    def get_upsell_products(self):
        """
        This method returns a list of products that can be upsold to the guest.
        """
        raise NotImplementedError


def get_pms(name: str) -> Type[PMSProvider]:
    """
    This function returns the PMS class for the given name.
    This does not return an instance of the class, but the class itself.
    Note, that the name should be the same as the class name without the 'PMS_' prefix.
    """
    assert name.isalpha()

    fullname = name.capitalize()
    # all new task managers should be included here
    base_module = "hotel.pms"

    for finder, module_name, is_pkg in pkgutil.walk_packages(importlib.import_module(base_module).__path__, base_module + "."):
        module = importlib.import_module(module_name)

        for name, obj in inspect.getmembers(module, inspect.isclass):
            # Check if the class matches the name and inherits from TaskManagerProvider
            if name == fullname and issubclass(obj, PMSProvider) and obj is not PMSProvider:
                return obj

    # Raise an error if no matching class is found
    raise ValueError(f"No such TaskManagerProvider class: {fullname}")