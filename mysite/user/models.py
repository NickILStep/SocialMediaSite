from django.db import models
from django.contrib.auth.models import User
import pytz

# Create your models here.
class Profile(models.Model):
    def __str__(self):
        return self.user.username

    UNITED_STATES_TIMEZONES = (
        ('US/Hawaii', 'Hawaii Standard Time'),
        ('US/Alaska', 'Alaska Standard Time'),
        ('US/Pacific', 'Pacific Standard Time'),
        ('US/Mountain', 'Mountain Standard Time'),
        ('US/Central', 'Central Standard Time'),
        ('US/Eastern', 'Eastern Standard Time')
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=1000, blank=True, null=True)
    location = models.CharField(max_length=50, blank=True, null=True)
    timezone = models.CharField(max_length=50, choices=UNITED_STATES_TIMEZONES, default='US/Mountain')
    birthday = models.DateField(blank=True, null=True)
    image = models.ImageField(default='profilepic.jpg', upload_to='profile_pictures')
    banner = models.ImageField(default='profilebanner.jpg', upload_to='profile_banners')
    savedPosts = models.ManyToManyField('feed.Post', related_name='savedPosts')
    likedPosts = models.ManyToManyField('feed.Post', related_name='likedPosts')
    following = models.ManyToManyField('self', related_name='following')
    followers = models.ManyToManyField('self', related_name='followers')


