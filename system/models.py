from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation
from django.conf import settings
from django.contrib.auth.models import User
from datetime import datetime, timedelta

class Activity(models.Model):
    FAVORITE = 'F'
    ACTIVITY_TYPES = (
        (FAVORITE, 'Favorite'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    activity_type = models.CharField(max_length=1, choices=ACTIVITY_TYPES)
    date = models.DateTimeField(auto_now_add=True)

    # Below the mandatory fields for generic relation
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()

    def __str__( self ):
        return 'Activity: %s, %s' % (self.user, self.activity_type)

# Create your models here.
class Shops( models.Model ):
    company_name = models.CharField(max_length=1000)
    address = models.CharField(max_length=1024)
    location = models.CharField(max_length=1024)
    postal_code = models.CharField(max_length=10)
    website = models.CharField(max_length=1000)
    facebook = models.CharField(max_length=1000)
    instagram = models.CharField(max_length=1000)
    phone_number = models.CharField(max_length=1000)
    email = models.CharField(max_length=1000)
    number_of_people_rated = models.IntegerField(default =0)
    categorization = models.CharField(max_length=256, default="others")
    region = models.CharField( max_length=128, default="")
    current_rating = models.IntegerField(default =0)
    #user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    favourite = GenericRelation(Activity, related_query_name='shops')

    def get_absolute_url(self):
        return reverse( 'system:detail', kwargs={'pk': self.pk} )

    def __str__( self ):
        return 'Company Name: %s, %s - %s' % (self.pk, self.company_name, self.address)

class Review( models.Model ):
    shop = models.ForeignKey( Shops, related_name="reviews_set", on_delete=models.CASCADE )
    user = models.CharField(max_length=250)
    body = models.TextField(default = "")
    rating = models.IntegerField(default = 5)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user

    def numberOfRating(self):
        return range(self.rating)

class Poll(models.Model):
    title = models.CharField(max_length=200, default='')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    expiry_date = models.DateTimeField(default=datetime.now())
    no_of_participant = models.IntegerField(default=2)
    current_participant = models.IntegerField(default=0)
    code = models.CharField(max_length=200)
    closed = models.BooleanField(default=False)
    deleted = models.BooleanField(default=False)

    def get_absolute_url(self):
        #return "/poll/%s" %(self.code)
        return reverse( 'system:poll_detail', kwargs={'code': self.code} )

class Choice(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE )
    shop = models.ForeignKey(Shops, on_delete=models.CASCADE )
    vote_count = models.IntegerField(default=0)

class Vote(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE )
    selected = models.ForeignKey(Choice, on_delete=models.CASCADE )
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True )
