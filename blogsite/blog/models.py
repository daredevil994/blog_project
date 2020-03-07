from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User

# Create your models
class Post(models.Model):
    # user=models.OneToOneField(User,on_delete=models.CASCADE,unique=True)
    author=models.ForeignKey('auth.User',on_delete=models.CASCADE)

    title=models.CharField(max_length=200)
    text=models.TextField()
    create_date=models.DateTimeField(default=timezone.now())
    publish_date=models.DateTimeField(blank=True,null=True)

    def publish(self):
        self.publish_date= timezone.now()
        self.save()

    def approve_comments(self):
        return self.comments.filter(approved_comment=True)

    def get_absolute_url(self):
        return reverse("post_detail",kwargs={'pk':self.pk})

    def __str__(self):
        return self.title

    # def __str__(self):
    #     return self.user.username


class Comment(models.Model):
    post=models.ForeignKey('blog.Post',related_name='comments',on_delete=models.CASCADE)
    author=models.CharField(max_length=200)
    text=models.TextField()
    create_date= models.DateTimeField(default=timezone.now())
    approved_comment=models.BooleanField(default=False)

    def approve(self):
        self.aproved_comment=True
        self.save()

    def get_absolute_url(self):
        return reverse('post_list')

    def __str___(self):
        return self.text
