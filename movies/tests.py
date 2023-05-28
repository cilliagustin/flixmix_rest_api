from django.contrib.auth.models import User
from .models import Movie
from rest_framework import status
from rest_framework.test import APITestCase


class MovieListViewTests(APITestCase):
    def setUp(self):
        User.objects.create_user(username='adam', password='pass')

    def test_can_list_movies(self):
        adam = User.objects.get(username='adam')
        Movie.objects.create(
            owner=adam, title='title', synopsis='synopsis',
            directors='Test Director', main_cast='Cast members',
            release_year=2000, movie_genre='crime'
            )
        response = self.client.get('/movies/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_logged_in_user_can_create_movie(self):
        self.client.login(username='adam', password='pass')
        response = self.client.post(
            '/movies/', {
                'title': 'title', 'synopsis': 'synopsis',
                'directors': 'Test Director', 'main_cast': 'Cast members',
                'release_year': 2000, 'movie_genre': 'crime'
                }
            )
        count = Movie.objects.count()
        self.assertEqual(count, 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_not_logged_in_cant_create_movie(self):
        response = self.client.post(
            '/movies/', {
                'title': 'title', 'synopsis': 'synopsis',
                'directors': 'Test Director', 'main_cast':
                'Cast members', 'release_year': 2000,
                'movie_genre': 'crime'
                }
            )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_usercan_not_create_movie_with_incomplete_data(self):
        response = self.client.post(
            '/movies/', {
                'directors': 'Test Director', 'main_cast': 'Cast members',
                'release_year': 2000, 'movie_genre': 'crime'
                }
            )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_can_retrieve_movie(self):
        adam = User.objects.get(username='adam')
        movie = Movie.objects.create(
            owner=adam, title='title', synopsis='synopsis',
            directors='Test Director', main_cast='Cast members',
            release_year=2000, movie_genre='crime'
            )
        response = self.client.get(f'/movies/{movie.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'title')

    def test_release_decade_is_created_correctly(self):
        adam = User.objects.get(username='adam')
        movie = Movie.objects.create(
            owner=adam, title='title',
            synopsis='synopsis', directors='Test Director',
            main_cast='Cast members', release_year=1997,
            movie_genre='crime'
            )
        response = self.client.get(f'/movies/{movie.id}/')
        self.assertIn('release_decade', response.data)
        self.assertEqual(response.data['release_decade'], 1990)


class MovieDetailViewTests(APITestCase):
    def setUp(self):
        adam = User.objects.create_user(username='adam', password='pass')
        adam.is_superuser = True
        adam.save()
        brian = User.objects.create_user(username='brian', password='pass')
        Movie.objects.create(
            owner=adam, title='title', synopsis='synopsis',
            directors='Test Director', main_cast='Cast members',
            release_year=2000, movie_genre='crime'
        )
        Movie.objects.create(
            owner=brian, title='other title', synopsis='other synopsis',
            directors='Test Director', main_cast='Cast members',
            release_year=2000, movie_genre='crime'
        )

    def test_can_retrieve_post_using_valid_id(self):
        response = self.client.get('/movies/1/')
        self.assertEqual(response.data['title'], 'title')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_cant_retrieve_post_using_invalid_id(self):
        response = self.client.get('/movies/3/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_admin_can_update_movie(self):
        self.client.login(username='adam', password='pass')
        movie = Movie.objects.filter(pk=2).first()
        response = self.client.put(
            f'/movies/2/', {
                'title': 'Updated Title',
                'synopsis': 'Updated Synopsis',
                'directors': 'Updated Directors',
                'main_cast': 'Updated Main Cast',
                'release_year': 2023,
                'movie_genre': 'crime'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated_movie = Movie.objects.get(pk=movie.id)
        self.assertEqual(updated_movie.title, 'Updated Title')

    def test_non_admin_can_not_update_movie(self):
        self.client.login(username='brian', password='pass')
        movie = Movie.objects.filter(pk=2).first()
        response = self.client.put(
            f'/movies/2/', {
                'title': 'Updated Title',
                'synopsis': 'Updated Synopsis',
                'directors': 'Updated Directors',
                'main_cast': 'Updated Main Cast',
                'release_year': 2023,
                'movie_genre': 'crime'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        updated_movie = Movie.objects.get(pk=movie.id)
        self.assertEqual(updated_movie.title, 'other title')

        def test_admin_can_delete_movie(self):
            self.client.login(username='adam', password='pass')
            movie = Movie.objects.get(pk=1)
            response = self.client.delete(f'/movies/{movie.id}/')
            self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

            # Check if the movie has been deleted from the database
            with self.assertRaises(Movie.DoesNotExist):
                Movie.objects.get(pk=movie.id)

        def test_non_admin_cannot_delete_movie(self):
            self.client.login(username='brian', password='pass')
            movie = Movie.objects.get(pk=1)
            response = self.client.delete(f'/movies/{movie.id}/')
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
            Movie.objects.get(pk=movie.id)
