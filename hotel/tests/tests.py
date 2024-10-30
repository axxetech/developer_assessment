import django.test

from hotel.models import Stay, Hotel

from hotel.tests import load_api_fixture
from hotel.tests.factories import HotelFactory, StayFactory


class PMS_Apaleotest(django.test.TestCase):
    def setUp(self) -> None:
        self.hotel = HotelFactory(pms=Hotel.PMS.APALEO)
        self.pms = self.hotel.get_pms()

    def test_clean_webhook_payload_faulty(self):
        cleaned_payload = self.pms.clean_webhook_payload(load_api_fixture("webhook_payload_faulty.json"))
        self.assertIsNone(cleaned_payload)

    def test_clean_webhook_payload(self):
        cleaned_payload = self.pms.clean_webhook_payload(load_api_fixture("webhook_payload.json"))
        if not cleaned_payload:
            self.fail("No cleaned payload returned")
        else:
            self.assertEqual(len(cleaned_payload["Events"]), 3)

    def test_handle_webhook(self):
        cleaned_payload = self.pms.clean_webhook_payload(load_api_fixture("webhook_payload.json"))
        success = self.pms.handle_webhook(cleaned_payload)
        self.assertTrue(success)
        stays = Stay.objects.filter(hotel=self.hotel)
        self.assertEqual(stays.count(), 3)

    def test_stay_has_breakfast(self):
        stay = StayFactory(hotel=self.hotel)
        self.assertIsNone(self.pms.stay_has_breakfast(stay))

        stay.pms_reservation_id = "7c22cb23-c517-48f9-a5d4-da811043bd67"
        stay.save()

        # Breakfast is either included or excluded, can be False or True
        self.assertIn(self.pms.stay_has_breakfast(stay), [False, True])
