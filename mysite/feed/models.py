from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Post(models.Model):
    def __str__(self):
        if len(self.content) > 50:
            return self.user.username + " -> " + self.title + ": " + self.content[0:50] + "..."
        else:
            return self.user.username + " -> " + self.title + ": " + self.content[0:50]

    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    title = models.CharField(max_length=50)
    content = models.TextField(max_length=2000)
    image = models.ImageField(default='postpic.jpg', upload_to='post_pictures')
    datetime = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField('user.Profile')

class Comment(models.Model):
    def __str__(self):
        return self.user.username + ": '" + self.title + "' on '" + self.post.title + "'"

    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, default=1)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)
    title = models.CharField(max_length=50)
    content = models.TextField(max_length=500)
    datetime = models.DateTimeField(auto_now_add=True)