from movies.models import Movie
from .models import Rating
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase


class RatingListTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='adam', password='pass'
            )
        self.brian = User.objects.create_user(
            username='brian', password='pass'
            )
        self.movie = Movie.objects.create(
            owner=self.user,  # Set the owner field with the user object
            title='Test Movie',
            release_year=2022,
            directors='Test Director',
            main_cast='Test Cast',
            movie_genre='crime'
        )
        Rating.objects.create(
            owner=self.user,
            movie=self.movie,
            value=5,
            title='Great Movie',
            content='This movie was amazing!'
        )

    def test_can_list_ratings(self):
        response = self.client.get('/ratings/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_logged_in_user_can_create_rating(self):
        data = {
            'movie': self.movie.pk,
            'value': 1,
            'title': 'Bad Movie',
            'content': 'This movie was terrible!'
        }
        self.client.force_authenticate(user=self.brian)
        response = self.client.post('/ratings/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Rating.objects.count(), 2)
        self.assertEqual(Rating.objects.filter(owner=self.brian).count(), 1)
        self.assertEqual(
            Rating.objects.filter(owner=self.brian).first().value, 1
            )

    def test_user_not_logged_in_cant_create_rating(self):
        response = self.client.post('/ratings/', {
            'movie': self.movie.id,
            'value': 3,
            'title': 'Average Movie',
            'content': 'It was okay.'
        })
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_cannot_create_rating_with_incomplete_data(self):
        self.client.login(username='adam', password='pass')
        response = self.client.post('/ratings/', {
            'movie': self.movie.id,
            'value': 5,
            'title': 'Great Movie'
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class RatingDetailViewTests(APITestCase):
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
        self.rating = Rating.objects.create(
            owner=self.adam,
            movie=self.movie,
            value=5,
            title='Great Movie',
            content='This movie was amazing!'
        )

    def test_can_retrieve_rating_using_valid_id(self):
        response = self.client.get(f'/ratings/{self.rating.pk}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['owner'], 'adam')
        self.assertEqual(response.data['value'], 5)

    def test_cant_retrieve_rating_using_invalid_id(self):
        response = self.client.get('/ratings/100/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_owner_can_update_rating(self):
        self.client.force_authenticate(user=self.adam)
        response = self.client.put(
            f'/ratings/{self.rating.pk}/',
            {
                'movie': self.movie.pk,
                'value': 4,
                'title': 'Updated Title',
                'content': 'Updated content'
            }
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated_rating = Rating.objects.get(pk=self.rating.pk)
        self.assertEqual(updated_rating.value, 4)

    def test_owner_can_delete_rating(self):
        self.client.force_authenticate(user=self.adam)
        response = self.client.delete(f'/ratings/{self.rating.pk}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Check if the rating has been deleted from the database
        with self.assertRaises(Rating.DoesNotExist):
            Rating.objects.get(pk=self.rating.pk)

    def test_admin_can_update_rating(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.put(
            f'/ratings/{self.rating.pk}/',
            {
                'movie': self.movie.pk,
                'value': 3,
                'title': 'Updated Title',
                'content': 'Updated content'
            }
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated_rating = Rating.objects.get(pk=self.rating.pk)
        self.assertEqual(updated_rating.value, 3)

    def test_admin_can_delete_rating(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.delete(f'/ratings/{self.rating.pk}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Check if the rating has been deleted from the database
        with self.assertRaises(Rating.DoesNotExist):
            Rating.objects.get(pk=self.rating.pk)

    def test_non_owner_cannot_update_rating(self):
        self.client.force_authenticate(user=self.brian)
        response = self.client.put(
            f'/ratings/{self.rating.pk}/',
            {
                'movie': self.movie.pk,
                'value': 2,
                'title': 'Updated Title',
                'content': 'Updated content'
            }
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        updated_rating = Rating.objects.get(pk=self.rating.pk)
        self.assertNotEqual(updated_rating.value, 2)

    def test_non_owner_cannot_delete_rating(self):
        self.client.force_authenticate(user=self.brian)
        response = self.client.delete(f'/ratings/{self.rating.pk}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        rating_exists = Rating.objects.filter(pk=self.rating.pk).exists()
        self.assertTrue(rating_exists)
