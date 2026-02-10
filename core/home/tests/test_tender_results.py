from django.test import TestCase
from home.models import TenderResults
from django.utils import timezone
from datetime import datetime
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
class TenderResultsTestCase(TestCase):
    def setUp(self):
        # Create one existing tender
        TenderResults.objects.create(
            tender_id="T123",
            bid_submission_end_date="07-02-2026",
            state_name="West Bengal"
        )
        self.url = reverse("login-page")
        self.user=User.objects.create_user(
            username="testuser",
            password="testpass123"
        )
        # self.url="/login-page/"

    def test_valid_login(self):
        # r=self.client.login(username="testuser", password="testpass123")
        # self.assertTrue(r)
        response=self.client.post(self.url,{"username":"testuser","password":"testpass123"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("token", response.data)
        self.assertEqual(response.data["username"], "testuser")

    def test_both_fields_match(self):
        """Should return True when both fields match"""
        exists = TenderResults.objects.filter(
            tender_id="T123",
            bid_submission_end_date="07-02-2026"
        ).exists()
        self.assertTrue(exists)

    def test_only_tender_id_match(self):
        """Should return False if only tender_id matches"""
        exists = TenderResults.objects.filter(
            tender_id="T123",
            bid_submission_end_date="08-02-2026"
        ).exists()
        self.assertFalse(exists)

    def test_only_date_match(self):
        """Should return False if only date matches"""
        exists = TenderResults.objects.filter(
            tender_id="T999",
            bid_submission_end_date="07-02-2026"
        ).exists()
        self.assertFalse(exists)

