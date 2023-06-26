from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Article
from .forms import ArticleForm


class BlogTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.article = Article.objects.create(
            title='Test Article',
            slug='test-article',
            body='This is a test article.',
            author=self.user
        )

    # check article_list returns successfully., using the right template
    def test_article_list_view(self):
        response = self.client.get(reverse('blog'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/article_list.html')

    