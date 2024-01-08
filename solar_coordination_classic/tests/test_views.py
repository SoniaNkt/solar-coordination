from django.test import TestCase, Client
from django.urls import reverse
from django.conf import settings


from django.contrib.auth.models import User
from solar_coordination_classic.models import Participant, Condition



class TestViews(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='test')
        self.password = 'test'
        self.user.set_password(self.password)
        self.user.save()

        self.condition = Condition.objects.create(ui_type='Chatbot First', group_size=4, active=True)
        self.condition.save()

        self.participant = Participant.objects.create(user=self.user, condition=self.condition)

    def test_welcome_view(self):
        url = reverse('welcome')  
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

    def test_unauthenticated_overview_view(self):
        protected_overview_url = reverse('overview')
        response = self.client.get(protected_overview_url)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login') + f'?next={protected_overview_url}')

    def test_authenticated_overview_view(self):
        self.client.force_login(self.user)

        response = self.client.get(reverse('overview'))
        self.assertEqual(response.status_code, 200)

    # def test_solar_and_booked_values(self):
