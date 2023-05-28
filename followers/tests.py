from django.contrib.auth.models import User
from django.db import models
from .models import Follower
from rest_framework import status
from rest_framework.test import APITestCase


class FollowerListTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.adam = User.objects.create_user(
            username='adam', password='password')
        cls.brian = User.objects.create_user(
            username='brian', password='password')
        cls.brad = User.objects.create_user(
            username='brad', password='password')
        Follower.objects.create(owner=cls.brian, followed=cls.adam)

    def test_can_list_follows(self):
        self.client.force_authenticate(user=self.adam)
        response = self.client.get('/followers/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)

    def test_Registered_user_can_follow(self):
        self.client.force_authenticate(user=self.brad)
        response = self.client.post('/followers/', {'followed': self.adam.pk})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Follower.objects.count(), 2)

    def test_Non_registered_user_cannot_follow(self):
        response = self.client.post('/followers/', {'followed': self.adam.pk})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Follower.objects.count(), 1)
