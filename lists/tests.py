from django.contrib.auth.models import User
from django.db import models
from movies.models import Movie
from .models import List
from rest_framework import status
from rest_framework.test import APITestCase


class ListViewTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='adam', password='pass')
        self.movie1 = Movie.objects.create(
            owner=self.user,
            title='Movie 1',
            release_year=2022,
            directors='Test Director',
            main_cast='Test Cast',
            movie_genre='crime'
        )
        self.movie2 = Movie.objects.create(
            owner=self.user,
            title='Movie 2',
            release_year=2022,
            directors='Test Director',
            main_cast='Test Cast',
            movie_genre='crime'
        )
        self.list = List.objects.create(
            owner=self.user,
            title='Test List',
            description='This is a test list'
        )
        self.list.movies.add(self.movie1, self.movie2)

    def test_can_list_lists(self):
        response = self.client.get('/lists/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_logged_in_user_can_create_list(self):
        data = {
            'owner': self.user.pk,
            'title': 'New List',
            'description': 'This is a new list',
            'movies': [self.movie1.pk, self.movie2.pk]
        }
        self.client.force_authenticate(user=self.user)
        response = self.client.post('/lists/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(List.objects.count(), 2)
        self.assertEqual(List.objects.filter(owner=self.user).count(), 2)

    def test_user_not_logged_in_cant_create_list(self):
        data = {
            'owner': self.user.pk,
            'title': 'New List',
            'description': 'This is a new list',
            'movies': [self.movie1.pk, self.movie2.pk]
        }
        response = self.client.post('/lists/', data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_cannot_create_list_with_incomplete_data(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post('/lists/', {
            'owner': self.user.pk,
            'title': 'Incomplete List',
            'description': 'This list is incomplete'
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class ListDetailViewTests(APITestCase):
    def setUp(self):
        self.admin = User.objects.create_user(
            username='admin', password='pass'
            )
        self.admin.is_superuser = True
        self.admin.save()
        self.adam = User.objects.create_user(
            username='adam', password='pass'
            )
        self.brian = User.objects.create_user(
            username='brian', password='pass'
            )
        self.movie = Movie.objects.create(
            owner=self.adam,
            title='Test Movie',
            release_year=2022,
            directors='Test Director',
            main_cast='Test Cast',
            movie_genre='crime'
        )
        self.list = List.objects.create(
            owner=self.adam,
            title='Test List',
            description='This is a test list'
        )
        self.list.movies.add(self.movie)

    def test_can_retrieve_list_using_valid_id(self):
        response = self.client.get(f'/lists/{self.list.pk}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['owner'], 'adam')
        self.assertEqual(response.data['title'], 'Test List')

    def test_cant_retrieve_list_using_invalid_id(self):
        response = self.client.get('/lists/100/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_owner_can_update_list(self):
        self.client.force_authenticate(user=self.adam)
        response = self.client.put(
            f'/lists/{self.list.pk}/',
            {
                'owner': self.adam.pk,
                'title': 'Updated Title',
                'description': 'Updated description',
                'movies': [self.movie.pk]
            }
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated_list = List.objects.get(pk=self.list.pk)
        self.assertEqual(updated_list.title, 'Updated Title')

    def test_owner_can_delete_list(self):
        self.client.force_authenticate(user=self.adam)
        response = self.client.delete(f'/lists/{self.list.pk}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        with self.assertRaises(List.DoesNotExist):
            List.objects.get(pk=self.list.pk)

    def test_admin_can_update_list(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.put(
            f'/lists/{self.list.pk}/',
            {
                'owner': self.adam.pk,
                'title': 'Updated Title',
                'description': 'Updated description',
                'movies': [self.movie.pk]
            }
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated_list = List.objects.get(pk=self.list.pk)
        self.assertEqual(updated_list.title, 'Updated Title')

    def test_admin_can_delete_list(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.delete(f'/lists/{self.list.pk}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        with self.assertRaises(List.DoesNotExist):
            List.objects.get(pk=self.list.pk)

    def test_non_owner_cannot_update_list(self):
        self.client.force_authenticate(user=self.brian)
        response = self.client.put(
            f'/lists/{self.list.pk}/',
            {
                'owner': self.adam.pk,
                'title': 'Updated Title',
                'description': 'Updated description',
                'movies': [self.movie.pk]
            }
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        updated_list = List.objects.get(pk=self.list.pk)
        self.assertNotEqual(updated_list.title, 'Updated Title')

    def test_non_owner_cannot_delete_list(self):
        self.client.force_authenticate(user=self.brian)
        response = self.client.delete(f'/lists/{self.list.pk}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        list_exists = List.objects.filter(pk=self.list.pk).exists()
        self.assertTrue(list_exists)
