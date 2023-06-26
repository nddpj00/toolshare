from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User, Permission
from .models import Article

class BlogTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.superuser = User.objects.create_superuser(username='admin', password='adminpassword')
        self.article = Article.objects.create(title='Test Article', slug='test-article', body='This is a test article.', author=self.user)


    # test checks for correct status code 200 for article_list
    def test_article_list_view(self):
        response = self.client.get(reverse('blog'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/article_list.html')
        self.assertContains(response, self.article.title)

    # test checks for correct status code 200 for article_detail
    def test_article_detail_view(self):
        response = self.client.get(reverse('detail', args=[self.article.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/article_detail.html')
        self.assertContains(response, self.article.title)

    #test adds a dummy article and checks its successfully added
    def test_add_article_view(self):
        self.client.login(username='admin', password='adminpassword')  # Log in as superuser
        response = self.client.get(reverse('add_article'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/add_article.html')

        data = {
            'title': 'New Article',
            'slug': 'new-article',
            'body': 'This is a new article.',
        }
        response = self.client.post(reverse('add_article'), data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Article.objects.count(), 2)
        self.assertEqual(Article.objects.latest('id').title, 'New Article')
    
    def test_edit_article_view(self):
        self.client.login(username='admin', password='adminpassword')  # Log in as superuser
        response = self.client.get(reverse('edit_article', args=[self.article.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/edit_article.html')

        data = {
            'title': 'Updated Article',
            'slug': 'updated-article',
            'body': 'This is an updated article.',
        }
        response = self.client.post(reverse('edit_article', args=[self.article.id]), data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Article.objects.get(id=self.article.id).title, 'Updated Article')
