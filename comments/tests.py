from django.contrib.auth.models import User
from django.db import models
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase
from .models import ListComment, RatingComment
from movies.models import Movie
from lists.models import List
from ratings.models import Rating


class ListCommentListTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='adam', password='pass')
        self.movie = Movie.objects.create(
            owner=self.user,
            title='Test Movie',
            release_year=2022,
            directors='Test Director',
            main_cast='Test Cast',
            movie_genre='crime'
        )
        self.list = List.objects.create(
            owner=self.user,
            title='Test List',
            description='This is a test list',
        )
        self.list.movies.set([self.movie])

    def test_can_list_comments(self):
        response = self.client.get('/listcomments/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_logged_in_user_can_create_comment(self):
        data = {
            'list': self.list.pk,
            'movie': self.movie.pk,
            'content': 'This list is great!'
        }
        self.client.force_authenticate(user=self.user)
        response = self.client.post('/listcomments/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ListComment.objects.count(), 1)
        self.assertEqual(
            ListComment.objects.filter(owner=self.user).count(), 1
            )
        self.assertEqual(
            ListComment.objects.filter(owner=self.user).first().content,
            'This list is great!'
        )

    def test_user_not_logged_in_cant_create_comment(self):
        response = self.client.post('/listcomments/', {
            'list': self.list.pk,
            'movie': self.movie.pk,
            'content': 'This list is awesome!'
        })
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_cannot_create_comment_with_incomplete_data(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post('/listcomments/', {
            'list': self.list.pk,
            'movie': self.movie.pk,
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class ListCommentDetailTest(APITestCase):
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
            owner=self.brian,
            title='Test Movie',
            release_year=2022,
            directors='Test Director',
            main_cast='Test Cast',
            movie_genre='crime'
        )
        self.list = List.objects.create(
            owner=self.adam,
            title='Test List',
            description='This is a test list',
        )
        self.list.movies.set([self.movie])
        self.list_comment = ListComment.objects.create(
            owner=self.adam,
            list=self.list,
            content='This is a test comment',
        )

    def test_can_retrieve_list_comment_using_valid_id(self):
        response = self.client.get(
            f'/listcomments/{self.list_comment.pk}/'
            )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['owner'], 'adam')
        self.assertEqual(
            response.data['content'], 'This is a test comment'
            )

    def test_cant_retrieve_list_comment_using_invalid_id(self):
        response = self.client.get(f'/listcomments/100/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_owner_can_delete_list_comment(self):
        self.client.force_authenticate(user=self.adam)
        response = self.client.delete(
            f'/listcomments/{self.list_comment.pk}/'
            )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        with self.assertRaises(ListComment.DoesNotExist):
            ListComment.objects.get(pk=self.list_comment.pk)

    def test_owner_can_update_list_comment(self):
        self.client.force_authenticate(user=self.adam)
        response = self.client.put(
            f'/listcomments/{self.list_comment.pk}/',
            {
                'owner': self.adam.id,
                'list': self.list.id,
                'content': 'Updated comment'
            },
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated_comment = ListComment.objects.get(pk=self.list_comment.pk)
        self.assertEqual(updated_comment.content, 'Updated comment')

    def test_admin_can_delete_list_comment(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.delete(
            f'/listcomments/{self.list_comment.pk}/'
            )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        with self.assertRaises(ListComment.DoesNotExist):
            ListComment.objects.get(pk=self.list_comment.pk)

    def test_admin_can_update_list_comment(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.put(
            f'/listcomments/{self.list_comment.pk}/',
            {
                'owner': self.adam.id,
                'list': self.list.id,
                'content': 'Updated comment'
            },
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated_comment = ListComment.objects.get(pk=self.list_comment.pk)
        self.assertEqual(updated_comment.content, 'Updated comment')

    def test_non_owner_cannot_update_list_comment(self):
        self.client.force_authenticate(user=self.brian)
        response = self.client.put(
            f'/listcomments/{self.list_comment.pk}/',
            {'content': 'Updated comment'}
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        updated_comment = ListComment.objects.get(pk=self.list_comment.pk)
        self.assertNotEqual(updated_comment.content, 'Updated comment')

    def test_non_owner_cannot_delete_list_comment(self):
        self.client.force_authenticate(user=self.brian)
        response = self.client.delete(
            f'/listcomments/{self.list_comment.pk}/'
            )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        comment_exists = ListComment.objects.filter(
            pk=self.list_comment.pk
            ).exists()
        self.assertTrue(comment_exists)


class RatingCommentListTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='adam', password='pass'
        )
        self.movie = Movie.objects.create(
            owner=self.user,
            title='Test Movie',
            release_year=2022,
            directors='Test Director',
            main_cast='Test Cast',
            movie_genre='crime'
        )
        self.rating = Rating.objects.create(
            owner=self.user,
            movie=self.movie,
            value=5,
            title='Great Movie',
            content='This movie was amazing!'
        )

    def test_can_list_comments(self):
        response = self.client.get('/ratingcomments/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_logged_in_user_can_create_comment(self):
        data = {
            'rating': self.rating.pk,
            'movie': self.movie.pk,
            'content': 'This review is great!'
        }
        self.client.force_authenticate(user=self.user)
        response = self.client.post('/ratingcomments/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(RatingComment.objects.count(), 1)
        self.assertEqual(
            RatingComment.objects.filter(owner=self.user).count(), 1
        )
        self.assertEqual(
            RatingComment.objects.filter(owner=self.user).first().content,
            'This review is great!'
        )

    def test_user_not_logged_in_cant_create_comment(self):
        response = self.client.post('/ratingcomments/', {
            'rating': self.rating.pk,
            'movie': self.movie.pk,
            'content': 'This review is great!'
        })
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_cannot_create_comment_with_incomplete_data(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post('/ratingcomments/', {
            'rating': self.rating.pk,
            'movie': self.movie.pk,
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class RatingCommentDetailTest(APITestCase):
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
            owner=self.brian,
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
        self.rating_comment = RatingComment.objects.create(
            owner=self.adam,
            rating=self.rating,
            content='This is a test comment',
        )

    def test_can_retrieve_rating_comment_using_valid_id(self):
        response = self.client.get(
            f'/ratingcomments/{self.rating_comment.pk}/'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['owner'], 'adam')
        self.assertEqual(
            response.data['content'], 'This is a test comment'
        )

    def test_cant_retrieve_rating_comment_using_invalid_id(self):
        response = self.client.get(f'/ratingcomments/100/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_owner_can_delete_rating_comment(self):
        self.client.force_authenticate(user=self.adam)
        response = self.client.delete(
            f'/ratingcomments/{self.rating_comment.pk}/'
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        with self.assertRaises(RatingComment.DoesNotExist):
            RatingComment.objects.get(pk=self.rating_comment.pk)

    def test_owner_can_update_rating_comment(self):
        self.client.force_authenticate(user=self.adam)
        response = self.client.put(
            f'/ratingcomments/{self.rating_comment.pk}/',
            {
                'owner': self.adam.id,
                'rating': self.rating.id,
                'content': 'Updated comment'
            },
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated_comment = RatingComment.objects.get(pk=self.rating_comment.pk)
        self.assertEqual(updated_comment.content, 'Updated comment')

    def test_admin_can_delete_rating_comment(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.delete(
            f'/ratingcomments/{self.rating_comment.pk}/'
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        with self.assertRaises(RatingComment.DoesNotExist):
            RatingComment.objects.get(pk=self.rating_comment.pk)

    def test_admin_can_update_rating_comment(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.put(
            f'/ratingcomments/{self.rating_comment.pk}/',
            {
                'owner': self.adam.id,
                'rating': self.rating.id,
                'content': 'Updated comment'
            },
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated_comment = RatingComment.objects.get(pk=self.rating_comment.pk)
        self.assertEqual(updated_comment.content, 'Updated comment')

    def test_non_owner_cannot_update_rating_comment(self):
        self.client.force_authenticate(user=self.brian)
        response = self.client.put(
            f'/ratingcomments/{self.rating_comment.pk}/',
            {'content': 'Updated comment'}
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        updated_comment = RatingComment.objects.get(pk=self.rating_comment.pk)
        self.assertNotEqual(updated_comment.content, 'Updated comment')

    def test_non_owner_cannot_delete_rating_comment(self):
        self.client.force_authenticate(user=self.brian)
        response = self.client.delete(
            f'/ratingcomments/{self.rating_comment.pk}/'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        comment_exists = RatingComment.objects.filter(
            pk=self.rating_comment.pk
        ).exists()
        self.assertTrue(comment_exists)
