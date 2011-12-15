import uuid
import urllib
import urlparse
from time import time
import oauth2 as oauth

from django.db import models
from django.contrib.auth.models import User

from consts import KEY_SIZE, SECRET_SIZE, CONSUMER_KEY_SIZE, CALLBACK_SIZE, CONSUMER_STATES,\
                   PENDING, VERIFIER_SIZE, MAX_URL_LENGTH, OUT_OF_BAND, NAME_SIZE

generate_random = User.objects.make_random_password

# The resource can be registered by user or auto assigned by system
class Resource(models.Model):
    name = models.CharField(max_length=NAME_SIZE)
    url = models.TextField(max_length=MAX_URL_LENGTH)
    is_readonly = models.BooleanField(default=True)
    
    #objects = ResourceManager()

    def __unicode__(self):
        return u"Resource %s with url %s" % (self.name, self.url)


class Consumer(models.Model):
    name = models.CharField(max_length=NAME_SIZE)
    desc = models.TextField()
    # this pair should be generated by system
    key = models.CharField(max_length=CONSUMER_KEY_SIZE, blank=True)
    secret = models.CharField(max_length=SECRET_SIZE, blank=True)

    status = models.SmallIntegerField(choices=CONSUMER_STATES, default=PENDING)
    user = models.ForeignKey(User, null=True, blank=True) # user can be set or not set, or can create a seperate table to store the relationship between user and consumer 

    target = models.CharField(max_length=CALLBACK_SIZE, blank=True) #if user only want to give request to specific consumer
    #objects = ConsumerManager()
    def __unicode__(self):
        return u"Consumer %s with key %s" % (self.name, self.key)
        

class Token(models.Model):
    REQUEST = 1
    ACCESS = 2
    FINISH = 3
    TOKEN_TYPES = ((REQUEST, u'Request'), (ACCESS, u'Access'), (FINISH, u'Finish'))
    
    key = models.CharField(max_length=KEY_SIZE, blank=True)
    token_type = models.SmallIntegerField(choices=TOKEN_TYPES)
    
    time_created = models.DateTimeField(auto_now_add=True)
    time_last = models.DateTimeField(auto_now=True)
    time_validate = models.IntegerField(default=0)
    mini_frequency = models.IntegerField(default=0)
    count_used = models.IntegerField(default=0)
    
    def __unicode__(self):
        return u"Token_%s_%s" % (self.key, self.get_token_type_display())
'''
auto update used_count
token.count_used = F("count_used") + 1
token.save()
refresh toaken
''' 

class TokenManager(models.Model):
    user = models.ForeignKey(User, null=True, blank=True)
    resource = models.ForeignKey(Resource, null=True)
    consumer = models.ForeignKey(Consumer, null=True)
    
    token_request = models.ForeignKey(Token, null=True, related_name='token_request')
    token_private = models.ForeignKey(Token, null=True, related_name='token_private')
    token_public = models.ForeignKey(Token, null=True, related_name='token_public')
    
    # used to modify token itself from consumer
    key = models.CharField(max_length=KEY_SIZE, blank=True)
    secret = models.CharField(max_length=SECRET_SIZE, blank=True)
    is_approved = models.BooleanField(default=False) # THIS MAY NOT BE NECESSARY
    
    callback = models.CharField(max_length=MAX_URL_LENGTH, blank=True)
    
    def __unicode__(self):
        return u"Token %s for %s from %s" % (self.key, self.consumer, self.user)
        
