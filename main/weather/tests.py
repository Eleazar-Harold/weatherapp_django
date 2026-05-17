# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from .models import City
from .forms import CityForm
from django.urls import reverse
from unittest.mock import patch

class CityModelTest(TestCase):
    def test_city_str(self):
        city = City.objects.create(name='London')
        self.assertEqual(str(city), 'London')

class CityFormTest(TestCase):
    def test_city_form_valid(self):
        form = CityForm(data={'name': 'London'})
        self.assertTrue(form.is_valid())

    def test_city_form_invalid(self):
        form = CityForm(data={'name': ''})
        self.assertFalse(form.is_valid())

class WeatherViewTest(TestCase):
    @patch('requests.get')
    @patch('os.environ.get')
    def test_index_get(self, mock_env, mock_get):
        mock_env.return_value = 'fake_api_key'
        # Mocking the response for index view's for loop
        # First, we need some cities in the DB to trigger the loop
        City.objects.create(name='London')
        
        mock_get.return_value.json.return_value = {
            'main': {'temp': 15},
            'weather': [{'description': 'broken clouds', 'icon': '04d'}],
            'cod': 200
        }
        
        # We need to set API_KEY in os.environ because the view uses os.environ['API_KEY'] directly, not os.environ.get
        with patch.dict('os.environ', {'API_KEY': 'fake_api_key'}):
            response = self.client.get(reverse('index'))
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'weather.html')
        self.assertContains(response, 'London')
        self.assertContains(response, '15')
        self.assertContains(response, 'broken clouds')

    @patch('requests.get')
    def test_index_post_add_city_success(self, mock_get):
        # The view makes two calls if POST and success: one for validation, one for the list
        mock_get.return_value.json.side_effect = [
            {'cod': '200'}, # for validation
            { # for listing
                'main': {'temp': 20},
                'weather': [{'description': 'clear sky', 'icon': '01d'}],
                'cod': 200
            }
        ]
        
        with patch.dict('os.environ', {'API_KEY': 'fake_api_key'}):
            response = self.client.post(reverse('index'), {'name': 'Paris'})
            
        self.assertEqual(City.objects.count(), 1)
        self.assertEqual(City.objects.first().name, 'Paris')

    @patch('requests.get')
    def test_index_post_add_city_invalid_api(self, mock_get):
        # API returns 404 for city not found
        mock_get.return_value.json.return_value = {'cod': '404'}
        
        with patch.dict('os.environ', {'API_KEY': 'fake_api_key'}):
            response = self.client.post(reverse('index'), {'name': 'InvalidCity'})
            
        self.assertEqual(City.objects.count(), 0)

    @patch('requests.get')
    def test_index_post_add_existing_city(self, mock_get):
        City.objects.create(name='London')
        # One call for listing (already in DB)
        mock_get.return_value.json.return_value = {
            'main': {'temp': 15},
            'weather': [{'description': 'broken clouds', 'icon': '04d'}],
            'cod': 200
        }
        
        with patch.dict('os.environ', {'API_KEY': 'fake_api_key'}):
            response = self.client.post(reverse('index'), {'name': 'London'})
            
        self.assertEqual(City.objects.count(), 1)
