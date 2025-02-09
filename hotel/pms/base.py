import importlib
import inspect
import logging
import pkgutil
from abc import ABC, abstractmethod
from typing import Optional, Type, TypedDict, Dict, Any, List

from django.db import transaction

from hotel.models import Hotel, UpsellProduct


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

    def get_upsell_products(self):
        """
        Template method for fetching, processing, and saving upsell products.

        The workflow is:
            1. Retrieve the raw upsell products from the PMS API.
            2. Parse the JSON response into a list of product models.
            3. (Optionally) Compare with the existing records and decide whether to update.
            4. Bulk save the products into the database.
        """

        products: List[UpsellProduct] = self.retrieve_products_api()
        saved_products = self.bulk_upsert(products)
        return saved_products

    def bulk_upsert(self, products: List[UpsellProduct]) -> bool:
        """
        Performs a bulk upsert on PMSRecord objects.

        :param products: A list of dictionaries, where each dictionary contains the fields
         for a PMSRecord instance. Each dictionary must include a unique key,
         e.g., 'external_id', used to identify existing records.
        """
        if not products:
            return  # Nothing to do

        # 1. Extract the list of unique identifiers from the incoming data.
        pms_ids = [product.pms_id for product in products]

        # 2. Retrieve any existing records from the database that have these unique ids.
        existing_records = UpsellProduct.objects.filter(pms_id__in=pms_ids)

        # 3. Build a lookup dict for fast access.
        existing_lookup = {record.pms_id: record for record in existing_records}

        # Prepare lists for records that need to be created or updated.
        records_to_create = []
        records_to_update = []

        # 4. Process each incoming record.
        for record_data in products:
            ext_id = record_data['external_id']
            if ext_id in existing_lookup:
                # Found an existing record – update its fields.
                record = existing_lookup[ext_id]
                # Loop over the keys to update the record.
                # (Optionally, skip fields that should not be updated.)
                for key, value in record_data.items():
                    setattr(record, key, value)
                records_to_update.append(record)
            else:
                # No record exists – create a new instance.
                records_to_create.append(UpsellProduct(**record_data))

        with transaction.atomic():
            if records_to_create:
                UpsellProduct.objects.bulk_create(records_to_create)
            if records_to_update:
                update_fields = [
                    field for field in products[0].keys() if field != "pms_id"
                ]
                UpsellProduct.objects.bulk_update(records_to_update, update_fields)

    @abstractmethod
    def retrieve_products_api(self) -> List[UpsellProduct]:
        """
        Perform the API call and return the raw JSON response.
        Concrete classes must implement this.
        """
        pass

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