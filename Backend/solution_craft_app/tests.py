from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from solution_craft_app.models import Ticket, User

class TicketAPITest(TestCase):
    def setUp(self):
        # Create a user
        self.user = User.objects.create(
            name="John Doe",
            email="john@example.com",
            role="Support Agent",
            hashed_password="hashed_password"
        )

        # Create a ticket
        self.ticket = Ticket.objects.create(
            customer_name="Jane Smith",
            email="jane@example.com",
            issue_description="Test issue description",
            status="Open",
            priority="High",
            assigned_to=self.user
        )

        # Valid ticket data for creating a new ticket
        self.valid_ticket_data = {
            "customer_name": "Alice Brown",
            "email": "alice@example.com",
            "issue_description": "New issue description",
            "status": "Open",
            "priority": "Low",
            "assigned_to": self.user.id
        }

    def test_create_ticket(self):
        url = reverse('ticket-list')  # Ensure this route is correct
        response = self.client.post(url, self.valid_ticket_data, content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['customer_name'], self.valid_ticket_data['customer_name'])

    def test_get_all_tickets(self):
        url = reverse('ticket-list')  # Ensure this route is correct
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_single_ticket(self):
        url = reverse('ticket-detail', args=[self.ticket.id])  # Ensure this route is correct
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['customer_name'], self.ticket.customer_name)

    def test_update_ticket(self):
        url = reverse('ticket-detail', args=[self.ticket.id])  # Ensure this route is correct
        updated_data = {
            "status": "Closed",
            "priority": "Low",
        }
        response = self.client.patch(url, updated_data, content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.ticket.refresh_from_db()
        self.assertEqual(self.ticket.status, "Closed")
        self.assertEqual(self.ticket.priority, "Low")

    def test_delete_ticket(self):
        url = reverse('ticket-detail', args=[self.ticket.id])  # Ensure this route is correct
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Ticket.objects.filter(id=self.ticket.id).exists())
        