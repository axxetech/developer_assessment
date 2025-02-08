from django.core.validators import MinValueValidator
from django.db import models


class Language(models.TextChoices):
    GERMAN = "de", "German"
    BRITISH_ENGLISH = "en-GB", "British English"
    SPANISH_SPAIN = "es-ES", "Spanish (Spain)"
    FRENCH = "fr", "French"
    ITALIAN = "it", "Italian"
    DUTCH = "nl", "Dutch"
    PORTUGUESE_PORTUGAL = "pt-PT", "Portuguese (Portugal)"
    SWEDISH = "sv", "Swedish"
    DANISH = "da", "Danish"


class Hotel(models.Model):
    class PMS(models.TextChoices):
        APALEO = "Apaleo", "Apaleo PMS"

    name = models.CharField(max_length=200)
    city = models.CharField(max_length=200, blank=False, null=False)
    pms = models.CharField(choices=PMS.choices, max_length=50, blank=True, null=True)
    pms_hotel_id = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.city} - {self.name}"

    def get_pms(self):
        pms_cls = get_pms(self.pms) if self.pms else None
        return pms_cls(self) if pms_cls else None


class UpsellProduct(models.Model):
    # Upsell product fields
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name="upsell_products")
    upsell_id = models.UUIDField(unique=True)  # Internal unique ID for the upsell product
    name = models.CharField(max_length=255)  # Name of the upsell product
    pms_id = models.CharField(max_length=255, null=True, blank=True)  # Optional PMS ID
    TYPE_CHOICES = [
        ("BREAKFAST", "Breakfast"),
        ("PARKING", "Parking"),
        ("OTHER", "Other"),
    ]
    type = models.CharField(max_length=50, choices=TYPE_CHOICES)

    # Bookable status
    is_bookable = models.BooleanField(default=True)

    # Age restrictions
    min_age = models.PositiveIntegerField(null=True, blank=True, validators=[MinValueValidator(0)])
    max_age = models.PositiveIntegerField(null=True, blank=True, validators=[MinValueValidator(0)])

    # Price and currency
    price = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3)  # ISO currency code (e.g., USD, EUR)

    # Per room or per guest configuration
    PER_WHOM_CHOICES = [
        ("ROOM", "Per Room"),
        ("GUEST", "Per Guest"),
    ]
    per_whom = models.CharField(max_length=10, choices=PER_WHOM_CHOICES)

    # Maximum cap for a single stay
    max_cap_per_stay = models.PositiveIntegerField(null=True, blank=True, validators=[MinValueValidator(1)])

    # Availability during the stay
    AVAILABILITY_CHOICES = [
        ("ENTIRE_STAY", "Entire Stay"),
        ("ON_ARRIVAL", "Only on Arrival"),
        ("ON_DEPARTURE", "Only on Departure"),
    ]
    availability_when = models.CharField(max_length=20, choices=AVAILABILITY_CHOICES)

    # Days when the product is offered
    OFFERED_DAY_CHOICES = [
        ("MON", "Monday"),
        ("TUE", "Tuesday"),
        ("WED", "Wednesday"),
        ("THU", "Thursday"),
        ("FRI", "Friday"),
        ("SAT", "Saturday"),
        ("SUN", "Sunday"),
        ("EVERYDAY", "Everyday"),
    ]
    offered_days = models.JSONField(default=list)  # Example: ["MON", "TUE", "FRI"]

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.type}) - {self.hotel.name}"


class Guest(models.Model):
    """
    Guests are identified by their phone number.
    """

    name = models.CharField(max_length=200)
    phone = models.CharField(
        max_length=200,
        unique=True,
    )
    language = models.CharField(max_length=5, choices=Language.choices, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Stay(models.Model):
    """
    One guest can stay in multiple hotels.
    One hotel can have multiple guests and multiple stays.
    Stays are unique by hotel and pms_reservation_id.
    """

    class Status(models.TextChoices):
        CANCEL = "cancel", "The guest has cancelled the reservation"
        BEFORE = "before", "The guest has not checked in yet"
        INSTAY = "instay", "The guest is currently in the hotel"
        AFTER = "after", "The guest has checked out"
        UNKNOWN = "unknown", "The status is unknown"

    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name="stays")
    guest = models.ForeignKey(Guest, on_delete=models.CASCADE, related_name="stays", blank=True, null=True)
    pms_reservation_id = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        help_text="The reservation ID from the Property Management System",
    )
    pms_guest_id = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        help_text="""The guest ID from the Property Management System.
        This is intended to be on Stay level, as the same person (phone) can stay in
        multiple hotels with different guest IDs.""",
    )
    status = models.CharField(choices=Status.choices, default=Status.UNKNOWN, max_length=50)
    checkin = models.DateField(blank=True, null=True)
    checkout = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("hotel", "pms_reservation_id")


from .pms.base import get_pms
