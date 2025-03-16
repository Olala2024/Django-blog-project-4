from django.test import TestCase
from django.urls import reverse
from .models import Contact
from .forms import ContactForm

class TestContactFormSubmission(TestCase):

    def test_contact_form_submission(self):
        contact_data = {
            "name": "Test User",
            "email": "testuser@example.com",
            "message": "This is a test message."
        }
        response = self.client.post(reverse('contact'), data=contact_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('contact'))

    def test_invalid_contact_form_submission(self):
        contact_data = {
            "name": "",
            "email": "testuser@example.com",
            "message": "This is a test message."
        }
        response = self.client.post(reverse('contact'), data=contact_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "blog/contact.html")
        self.assertContains(response, "This field is required.")