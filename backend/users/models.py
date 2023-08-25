from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    first_name = models.CharField(
        'First name',
        max_length=150,
    )
    last_name = models.CharField(
        'Last name',
        max_length=150,
    )
    email = models.EmailField(
        'Email',
        unique=True,
        max_length=254,
    )
    username = models.CharField(
        'Username',
        max_length=150,
        unique=True,
    )
    password = models.CharField(
        'Password',
        max_length=150,
    )

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.username


class Subscribe(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Subscriber'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Subscribing'
    )

    def __str__(self):
        return f'{self.user.username} -> {self.author.username}'

    class Meta:
        ordering = ['user']
