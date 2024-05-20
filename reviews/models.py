from django.db import models

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
    review_content = models.TextField()
    # user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    # store_id = models.ForeignKey(Store, on_delete=models.CASCADE)
    # store_name = models.ForeignKey(Store, on_delete=models.CASCADE)
    score = models.CharField(max_length=5, choices = SCORE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Comment(models.Model):
    review_id = models.ForeignKey(Review, on_delete=models.CASCADE)
    # user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)