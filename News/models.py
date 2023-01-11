from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    author_rating = models.IntegerField(default=0)

    def update_rating(self):
        author_posts_rating = Post.objects.all().filter(author_id=self.pk).aggregate(
            posts_rating_sum=Sum('post_rating') * 3)
        author_comments_rating = Comment.objects.all().filter(user_id=self.user).aggregate(
            comments_rating_sum=Sum('comment_rating'))

        print(author_posts_rating)
        print(author_comments_rating)

        self.author_rating = author_posts_rating['posts_rating_sum'] + author_comments_rating['comments_rating_sum']
        self.save()

    def __str__(self):
        return f'{self.user.username}'


class Category(models.Model):
    article = 'AE'
    news = 'NS'
    POSITIONS = [
        (article, 'Статья'),
        (news, 'Новости')
    ]
    title = models.CharField(max_length=200, unique=True)
    positions = models.CharField(max_length=7, choices=POSITIONS, default=None)

    def __str__(self):
        return self.name.title()


class Post(models.Model):
    article = 'AE'
    news = 'NS'
    CHOICES = [
        (article, 'Статья'),
        (news, 'Новости')
    ]
    _author = models.ForeignKey(Author, on_delete=models.CASCADE)
    choice = models.CharField(max_length=10, choices=CHOICES)
    post_time = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField(Category, through='PostCategory')
    head = models.TextField(db_column='Заголовок')
    text = models.TextField(db_column='Текст')
    rating = models.PositiveIntegerField(default=0)
    post_rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self, length=124):
        return f"{self.text[:length]}..." if len(str(self.text)) > length else self.text


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()


