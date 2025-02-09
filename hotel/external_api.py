import json
import random
import uuid
import datetime

"""
This document simulates the external API that our system uses to communicate with the
booking systems from hotels (Property Management Systems). Use the below functions to
simulate the communication with the external API.
"""


class APIError(Exception):
    pass


reservation_statuses = [
    "in_house",
    "checked_out",
    "cancelled",
    "no_show",
    "not_confirmed",
    "booked",
]


def get_reservations_for_given_checkin_date(checkin_date: str) -> str:
    """
    Returns reservations for a given checkin date.
    The reservations are returned as a JSON string.
    Note, the checkin date is a string in the format YYYY-MM-DD.
    This is just to simulate the external API.
    """

    assert isinstance(checkin_date, str), "checkin_date should be a string."
    assert datetime.datetime.strptime(checkin_date, "%Y-%m-%d"), "checkin_date should have the format: YYYY-MM-DD."

    # This API call can fail randomly, just to simulate a real API.
    if random.randint(0, 10) == 0:
        raise APIError("The API is temporarily not available. Please try again.")

    return json.dumps(
        [
            {
                "HotelId": "851df8c8-90f2-4c4a-8e01-a4fc46b25178",
                "ReservationId": str(uuid.uuid4()),
                "GuestId": str(uuid.uuid4()),
                "Status": reservation_statuses[random.randint(0, len(reservation_statuses) - 1)],
                "CheckInDate": checkin_date,
                "CheckOutDate": (
                    datetime.datetime.strptime(checkin_date, "%Y-%m-%d")
                    + datetime.timedelta(days=random.randint(1, 10))
                ).strftime("%Y-%m-%d"),
                "BreakfastIncluded": random.choice([True, False]),
                "RoomNumber": random.randint(1, 100),
            }
            for _ in range(random.randint(1, 10))
        ]
    )


def get_reservation_details(reservation_id: str) -> str:
    """
    Returns the reservation details for any given reservation ID.
    The reservation details are returned as a JSON string.
    """

    # This API call can fail randomly, just to simulate a real API.
    if random.randint(0, 10) == 0:
        raise APIError("The API is temporarily not available. Please try again.")

    return json.dumps(
        {
            "HotelId": "851df8c8-90f2-4c4a-8e01-a4fc46b25178",
            "ReservationId": reservation_id,
            "GuestId": str(uuid.uuid4()),
            "Status": reservation_statuses[random.randint(0, len(reservation_statuses) - 1)],
            "CheckInDate": (datetime.date.today() - datetime.timedelta(days=random.randint(0, 10))).strftime(
                "%Y-%m-%d"
            ),
            "CheckOutDate": (datetime.date.today() + datetime.timedelta(days=random.randint(1, 10))).strftime(
                "%Y-%m-%d"
            ),
            "BreakfastIncluded": random.choice([True, False]),
            "RoomNumber": random.randint(1, 100),
        }
    )


def get_guest_details(guest_id: str) -> str:
    """
    Returns the guest details for any given guest ID.
    The guest details are returned as a JSON string.
    """

    # This API call can fail randomly, just to simulate a real API.
    if random.randint(0, 10) == 0:
        raise APIError("The API is temporarily not available. Please try again.")

    countries = ["NL", "DE", "GG", "GB", "", "CA", "BR", "CN", None, "AU"]
    names = [
        "John Doe",
        "Jane Doe",
        "John Smith",
        "Jane Smith",
        "",
        "Izzy",
        "Sara",
        "Bob",
        "Alice",
        None,
    ]
    phones = [
        "+491234567890",
        "123",
        "0123456789",
        "+442071234567",
        "Not available",
        "+16041234567",
        "",
        "+8612345678901",
        None,
        "+61491570156",
    ]

    return json.dumps(
        {
            "GuestId": guest_id,
            "Name": names[random.randint(0, len(names) - 1)],
            "Phone": phones[random.randint(0, len(phones) - 1)],
            "Country": countries[random.randint(0, len(countries) - 1)],
        }
    )


def get_apaleo_upsell_products():
    """
    Returns a dictionary containing upsell products with their details.
    """
    upsell_products = {
        "services": [
            {
                "id": "MUC-BRKF",
                "name": "Breakfast",
                "code": "BRKF",
                "description": "Enjoy fresh fruit, just-baked viennoiseries, or a hearty morning meal.",
                "defaultGrossPrice": {
                    "amount": 20.00,
                    "currency": "EUR"
                },
                "pricingUnit": "Person",
                "postNextDay": True,
                "serviceType": "FoodAndBeverages",
                "vatType": "Normal",
                "availability": {
                    "mode": "Daily",
                    "daysOfWeek": [
                        "Monday",
                        "Tuesday",
                        "Wednesday",
                        "Thursday",
                        "Friday",
                        "Saturday",
                        "Sunday"
                    ]
                },
                "property": {
                    "id": "MUC"
                },
                "channelCodes": [
                    "Direct",
                    "BookingCom",
                    "Ibe",
                    "ChannelManager"
                ]
            },
            {
                "id": "BER-BRKF",
                "name": "Breakfast",
                "code": "BRKF",
                "description": "Enjoy fresh fruit, just-baked viennoiseries, or a hearty morning meal.",
                "defaultGrossPrice": {
                    "amount": 15.00,
                    "currency": "EUR"
                },
                "pricingUnit": "Person",
                "postNextDay": True,
                "serviceType": "FoodAndBeverages",
                "vatType": "Normal",
                "availability": {
                    "mode": "Daily",
                    "daysOfWeek": [
                        "Monday",
                        "Tuesday",
                        "Wednesday",
                        "Thursday",
                        "Friday",
                        "Saturday",
                        "Sunday"
                    ]
                },
                "property": {
                    "id": "BER"
                },
                "channelCodes": [
                    "Direct",
                    "BookingCom",
                    "Ibe",
                    "ChannelManager"
                ],
                "ageCategoryId": "BER-ADULTS"
            },
            {
                "id": "VIE-BRKF",
                "name": "Breakfast",
                "code": "BRKF",
                "description": "Enjoy fresh fruit, just-baked viennoiseries, or a hearty morning meal.",
                "defaultGrossPrice": {
                    "amount": 15.00,
                    "currency": "EUR"
                },
                "pricingUnit": "Person",
                "postNextDay": True,
                "serviceType": "FoodAndBeverages",
                "vatType": "Normal",
                "availability": {
                    "mode": "Daily",
                    "daysOfWeek": [
                        "Monday",
                        "Tuesday",
                        "Wednesday",
                        "Thursday",
                        "Friday",
                        "Saturday",
                        "Sunday"
                    ]
                },
                "property": {
                    "id": "VIE"
                },
                "channelCodes": [
                    "Direct",
                    "BookingCom",
                    "Ibe",
                    "ChannelManager"
                ]
            },
            {
                "id": "LND-BRKF",
                "name": "Breakfast",
                "code": "BRKF",
                "description": "Enjoy fresh fruit, just-baked viennoiseries, or a hearty morning meal.",
                "defaultGrossPrice": {
                    "amount": 20.00,
                    "currency": "GBP"
                },
                "pricingUnit": "Person",
                "postNextDay": True,
                "serviceType": "FoodAndBeverages",
                "vatType": "Normal",
                "availability": {
                    "mode": "Daily",
                    "daysOfWeek": [
                        "Monday",
                        "Tuesday",
                        "Wednesday",
                        "Thursday",
                        "Friday",
                        "Saturday",
                        "Sunday"
                    ]
                },
                "property": {
                    "id": "LND"
                },
                "channelCodes": [
                    "Direct",
                    "BookingCom",
                    "Ibe",
                    "ChannelManager"
                ]
            },
            {
                "id": "PAR-BRKF",
                "name": "Breakfast",
                "code": "BRKF",
                "description": "Enjoy fresh fruit, just-baked viennoiseries, or a hearty morning meal.",
                "defaultGrossPrice": {
                    "amount": 15.00,
                    "currency": "EUR"
                },
                "pricingUnit": "Person",
                "postNextDay": True,
                "serviceType": "FoodAndBeverages",
                "vatType": "Normal",
                "availability": {
                    "mode": "Daily",
                    "daysOfWeek": [
                        "Monday",
                        "Tuesday",
                        "Wednesday",
                        "Thursday",
                        "Friday",
                        "Saturday",
                        "Sunday"
                    ]
                },
                "property": {
                    "id": "PAR"
                },
                "channelCodes": [
                    "Direct",
                    "BookingCom",
                    "Ibe",
                    "ChannelManager"
                ]
            },
            {
                "id": "BER-BRKFK",
                "name": " Breakfast Kids",
                "code": "BRKFK",
                "description": "\nBreakfast kids\n",
                "defaultGrossPrice": {
                    "amount": 5.00,
                    "currency": "EUR"
                },
                "pricingUnit": "Person",
                "postNextDay": True,
                "serviceType": "FoodAndBeverages",
                "vatType": "Normal",
                "availability": {
                    "mode": "Daily",
                    "daysOfWeek": [
                        "Sunday",
                        "Monday",
                        "Tuesday",
                        "Wednesday",
                        "Thursday",
                        "Friday",
                        "Saturday"
                    ]
                },
                "property": {
                    "id": "BER"
                },
                "channelCodes": [
                    "Direct",
                    "BookingCom",
                    "ChannelManager"
                ],
                "ageCategoryId": "BER-BRKK"
            },
            {
                "id": "BER-BRKFT",
                "name": " Breakfast Teen",
                "code": "BRKFT",
                "description": "\nBreakfast\n",
                "defaultGrossPrice": {
                    "amount": 10.00,
                    "currency": "EUR"
                },
                "pricingUnit": "Person",
                "postNextDay": True,
                "serviceType": "FoodAndBeverages",
                "vatType": "Normal",
                "availability": {
                    "mode": "Daily",
                    "daysOfWeek": [
                        "Sunday",
                        "Monday",
                        "Tuesday",
                        "Wednesday",
                        "Thursday",
                        "Friday",
                        "Saturday"
                    ]
                },
                "property": {
                    "id": "BER"
                },
                "channelCodes": [
                    "BookingCom",
                    "Direct",
                    "ChannelManager"
                ],
                "ageCategoryId": "BER-BRKT"
            },
            {
                "id": "MUC-CLEANING",
                "name": "Final cleaning",
                "code": "CLEANING",
                "description": "Final cleaning.",
                "defaultGrossPrice": {
                    "amount": 30.00,
                    "currency": "EUR"
                },
                "pricingUnit": "Person",
                "postNextDay": True,
                "serviceType": "Other",
                "vatType": "Normal",
                "availability": {
                    "mode": "Departure",
                    "daysOfWeek": [
                        "Monday",
                        "Tuesday",
                        "Wednesday",
                        "Thursday",
                        "Friday",
                        "Saturday",
                        "Sunday"
                    ]
                },
                "property": {
                    "id": "MUC"
                },
                "channelCodes": [
                    "Direct",
                    "BookingCom",
                    "Ibe",
                    "ChannelManager"
                ]
            },
            {
                "id": "BER-CLEANING",
                "name": "Final cleaning",
                "code": "CLEANING",
                "description": "Final cleaning.",
                "defaultGrossPrice": {
                    "amount": 30.00,
                    "currency": "EUR"
                },
                "pricingUnit": "Person",
                "postNextDay": True,
                "serviceType": "Other",
                "vatType": "Normal",
                "availability": {
                    "mode": "Departure",
                    "daysOfWeek": [
                        "Monday",
                        "Tuesday",
                        "Wednesday",
                        "Thursday",
                        "Friday",
                        "Saturday",
                        "Sunday"
                    ]
                },
                "property": {
                    "id": "BER"
                },
                "channelCodes": [
                    "Direct",
                    "BookingCom",
                    "Ibe",
                    "ChannelManager"
                ]
            },
            {
                "id": "VIE-CLEANING",
                "name": "Final cleaning",
                "code": "CLEANING",
                "description": "Final cleaning.",
                "defaultGrossPrice": {
                    "amount": 30.00,
                    "currency": "EUR"
                },
                "pricingUnit": "Person",
                "postNextDay": True,
                "serviceType": "Other",
                "vatType": "Normal",
                "availability": {
                    "mode": "Departure",
                    "daysOfWeek": [
                        "Monday",
                        "Tuesday",
                        "Wednesday",
                        "Thursday",
                        "Friday",
                        "Saturday",
                        "Sunday"
                    ]
                },
                "property": {
                    "id": "VIE"
                },
                "channelCodes": [
                    "Direct",
                    "BookingCom",
                    "Ibe",
                    "ChannelManager"
                ]
            },
            {
                "id": "PAR-CLEANING",
                "name": "Final cleaning",
                "code": "CLEANING",
                "description": "Final cleaning.",
                "defaultGrossPrice": {
                    "amount": 30.00,
                    "currency": "EUR"
                },
                "pricingUnit": "Person",
                "postNextDay": True,
                "serviceType": "Other",
                "vatType": "Normal",
                "availability": {
                    "mode": "Departure",
                    "daysOfWeek": [
                        "Monday",
                        "Tuesday",
                        "Wednesday",
                        "Thursday",
                        "Friday",
                        "Saturday",
                        "Sunday"
                    ]
                },
                "property": {
                    "id": "PAR"
                },
                "channelCodes": [
                    "Direct",
                    "BookingCom",
                    "Ibe",
                    "ChannelManager"
                ]
            },
            {
                "id": "VIE-DRINK",
                "name": "Welcome drink",
                "code": "DRINK",
                "description": "Enjoy a welcome drink at our bar on arrival.",
                "defaultGrossPrice": {
                    "amount": 7.50,
                    "currency": "EUR"
                },
                "pricingUnit": "Person",
                "postNextDay": False,
                "serviceType": "FoodAndBeverages",
                "vatType": "Normal",
                "availability": {
                    "mode": "Arrival",
                    "daysOfWeek": [
                        "Monday",
                        "Tuesday",
                        "Wednesday",
                        "Thursday",
                        "Friday",
                        "Saturday",
                        "Sunday"
                    ]
                },
                "property": {
                    "id": "VIE"
                },
                "channelCodes": [
                    "Direct",
                    "BookingCom",
                    "Ibe",
                    "ChannelManager"
                ]
            },
            {
                "id": "PAR-DRINK",
                "name": "Welcome drink",
                "code": "DRINK",
                "description": "Enjoy a welcome drink at our bar on arrival.",
                "defaultGrossPrice": {
                    "amount": 7.50,
                    "currency": "EUR"
                },
                "pricingUnit": "Person",
                "postNextDay": False,
                "serviceType": "FoodAndBeverages",
                "vatType": "Normal",
                "availability": {
                    "mode": "Arrival",
                    "daysOfWeek": [
                        "Monday",
                        "Tuesday",
                        "Wednesday",
                        "Thursday",
                        "Friday",
                        "Saturday",
                        "Sunday"
                    ]
                },
                "property": {
                    "id": "PAR"
                },
                "channelCodes": [
                    "Direct",
                    "BookingCom",
                    "Ibe",
                    "ChannelManager"
                ]
            },
            {
                "id": "MUC-DRINK",
                "name": "Welcome drink",
                "code": "DRINK",
                "description": "Enjoy a welcome drink at our bar on arrival.",
                "defaultGrossPrice": {
                    "amount": 7.50,
                    "currency": "EUR"
                },
                "pricingUnit": "Person",
                "postNextDay": False,
                "serviceType": "FoodAndBeverages",
                "vatType": "Normal",
                "availability": {
                    "mode": "Arrival",
                    "daysOfWeek": [
                        "Monday",
                        "Tuesday",
                        "Wednesday",
                        "Thursday",
                        "Friday",
                        "Saturday",
                        "Sunday"
                    ]
                },
                "property": {
                    "id": "MUC"
                },
                "channelCodes": [
                    "Direct",
                    "BookingCom",
                    "Ibe",
                    "ChannelManager"
                ]
            },
            {
                "id": "BER-DRINK",
                "name": "Welcome drink",
                "code": "DRINK",
                "description": "Enjoy a welcome drink at our bar on arrival.",
                "defaultGrossPrice": {
                    "amount": 7.50,
                    "currency": "EUR"
                },
                "pricingUnit": "Person",
                "postNextDay": False,
                "serviceType": "FoodAndBeverages",
                "vatType": "Normal",
                "availability": {
                    "mode": "Arrival",
                    "daysOfWeek": [
                        "Monday",
                        "Tuesday",
                        "Wednesday",
                        "Thursday",
                        "Friday",
                        "Saturday",
                        "Sunday"
                    ]
                },
                "property": {
                    "id": "BER"
                },
                "channelCodes": [
                    "Direct",
                    "BookingCom",
                    "Ibe",
                    "ChannelManager"
                ]
            },
            {
                "id": "VIE-WLAN",
                "name": "High-Speed WLAN",
                "code": "WLAN",
                "description": "Upgrade the complimentary internet access to a high speed connection.",
                "defaultGrossPrice": {
                    "amount": 5.00,
                    "currency": "EUR"
                },
                "pricingUnit": "Room",
                "postNextDay": False,
                "serviceType": "Other",
                "vatType": "Normal",
                "availability": {
                    "mode": "Daily",
                    "daysOfWeek": [
                        "Monday",
                        "Tuesday",
                        "Wednesday",
                        "Thursday",
                        "Friday",
                        "Saturday",
                        "Sunday"
                    ]
                },
                "property": {
                    "id": "VIE"
                },
                "channelCodes": [
                    "Direct",
                    "BookingCom",
                    "Ibe",
                    "ChannelManager"
                ]
            },
            {
                "id": "LND-WLAN",
                "name": "High-Speed WLAN",
                "code": "WLAN",
                "description": "Upgrade the complimentary internet access to a high speed connection.",
                "defaultGrossPrice": {
                    "amount": 10.00,
                    "currency": "GBP"
                },
                "pricingUnit": "Room",
                "postNextDay": False,
                "serviceType": "Other",
                "vatType": "Normal",
                "availability": {
                    "mode": "Daily",
                    "daysOfWeek": [
                        "Monday",
                        "Tuesday",
                        "Wednesday",
                        "Thursday",
                        "Friday",
                        "Saturday",
                        "Sunday"
                    ]
                },
                "property": {
                    "id": "LND"
                },
                "channelCodes": [
                    "Direct",
                    "BookingCom",
                    "Ibe",
                    "ChannelManager"
                ]
            },
            {
                "id": "PAR-WLAN",
                "name": "High-Speed WLAN",
                "code": "WLAN",
                "description": "Upgrade the complimentary internet access to a high speed connection.",
                "defaultGrossPrice": {
                    "amount": 5.00,
                    "currency": "EUR"
                },
                "pricingUnit": "Room",
                "postNextDay": False,
                "serviceType": "Other",
                "vatType": "Normal",
                "availability": {
                    "mode": "Daily",
                    "daysOfWeek": [
                        "Monday",
                        "Tuesday",
                        "Wednesday",
                        "Thursday",
                        "Friday",
                        "Saturday",
                        "Sunday"
                    ]
                },
                "property": {
                    "id": "PAR"
                },
                "channelCodes": [
                    "Direct",
                    "BookingCom",
                    "Ibe",
                    "ChannelManager"
                ]
            },
            {
                "id": "MUC-WLAN",
                "name": "High-Speed WLAN",
                "code": "WLAN",
                "description": "Upgrade the complimentary internet access to a high speed connection.",
                "defaultGrossPrice": {
                    "amount": 10.00,
                    "currency": "EUR"
                },
                "pricingUnit": "Room",
                "postNextDay": False,
                "serviceType": "Other",
                "vatType": "Normal",
                "availability": {
                    "mode": "Daily",
                    "daysOfWeek": [
                        "Monday",
                        "Tuesday",
                        "Wednesday",
                        "Thursday",
                        "Friday",
                        "Saturday",
                        "Sunday"
                    ]
                },
                "property": {
                    "id": "MUC"
                },
                "channelCodes": [
                    "Direct",
                    "BookingCom",
                    "Ibe",
                    "ChannelManager"
                ]
            },
            {
                "id": "BER-WLAN",
                "name": "High-Speed WLAN",
                "code": "WLAN",
                "description": "Upgrade the complimentary internet access to a high speed connection.",
                "defaultGrossPrice": {
                    "amount": 5.00,
                    "currency": "EUR"
                },
                "pricingUnit": "Room",
                "postNextDay": False,
                "serviceType": "Other",
                "vatType": "Normal",
                "availability": {
                    "mode": "Daily",
                    "daysOfWeek": [
                        "Monday",
                        "Tuesday",
                        "Wednesday",
                        "Thursday",
                        "Friday",
                        "Saturday",
                        "Sunday"
                    ]
                },
                "property": {
                    "id": "BER"
                },
                "channelCodes": [
                    "Direct",
                    "BookingCom",
                    "Ibe",
                    "ChannelManager"
                ]
            },
            {
                "id": "MUC-YOGA",
                "name": "Sun Salutation",
                "code": "YOGA",
                "description": "Start the day with a private Yoga session with one of our certified trainers.",
                "defaultGrossPrice": {
                    "amount": 60.00,
                    "currency": "EUR"
                },
                "pricingUnit": "Room",
                "postNextDay": True,
                "serviceType": "Other",
                "vatType": "Normal",
                "availability": {
                    "mode": "Daily",
                    "daysOfWeek": [
                        "Monday",
                        "Tuesday",
                        "Wednesday",
                        "Thursday",
                        "Friday",
                        "Saturday",
                        "Sunday"
                    ]
                },
                "property": {
                    "id": "MUC"
                },
                "channelCodes": [
                    "Direct",
                    "BookingCom",
                    "Ibe",
                    "ChannelManager"
                ]
            },
            {
                "id": "LND-YOGA",
                "name": "Sun Salutation",
                "code": "YOGA",
                "description": "Start the day with a private Yoga session with one of our certified trainers.",
                "defaultGrossPrice": {
                    "amount": 60.00,
                    "currency": "GBP"
                },
                "pricingUnit": "Room",
                "postNextDay": True,
                "serviceType": "Other",
                "vatType": "Normal",
                "availability": {
                    "mode": "Daily",
                    "daysOfWeek": [
                        "Monday",
                        "Tuesday",
                        "Wednesday",
                        "Thursday",
                        "Friday",
                        "Saturday",
                        "Sunday"
                    ]
                },
                "property": {
                    "id": "LND"
                },
                "channelCodes": [
                    "Direct",
                    "BookingCom",
                    "Ibe",
                    "ChannelManager"
                ]
            }
        ],
        "count": 22
    }
    return upsell_products
