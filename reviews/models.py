from django.db import models

from accounts.models import Accounts
from stores.models import Store

class Review(models.Model):
    SCORE_CHOICES = (
        ('1', 1),
        ('1.5', 1.5),
        ('2', 2),
        ('2.5', 2.5),
        ('3', 3),
        ('3.5', 3.5),
        ('4', 4),
        ('4.5', 4.5),
        ('5', 5),
    )
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    user = models.ForeignKey(Accounts, on_delete=models.CASCADE)
    review_content = models.TextField()
    score = models.CharField(max_length=5, choices = SCORE_CHOICES)
    image = models.ImageField(upload_to='reviews/image/%Y/%m/%d')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Comment(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE)
    user = models.ForeignKey(Accounts, on_delete=models.CASCADE)
    comment_content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)