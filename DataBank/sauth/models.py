from django.db import models
from django.contrib.auth.models import User
import util as sutil
# Create your models here.


class Object(models.Model):
    type = models.SmallIntegerField(choices=sutil.OBJECT_TYPES, default=sutil.OBJECT_TYPE_RESOURCE, null=False)
    resource = models.CharField(max_length=sutil.OBJECT_RESOURCE_SIZE, null=True, blank=True)
    token = models.ForeignKey('Token', null=True, blank=True)
    
    name = models.CharField(max_length=sutil.NAME_SIZE, null=False)
    alias = models.CharField(max_length=sutil.ALIAS_SIZE, null=True, blank=True)   
    permission =  models.SmallIntegerField(choices=sutil.OBJECT_PERMISSIONS, default=sutil.OBJECT_PERMISSION_READ, null=False)
    description = models.CharField(max_length=sutil.DESCRIPTION_SIZE, null=True, blank=True)
    
    def __unicode__(self):
        return u"Object name=%s type=%s permission=%s" %(self.name, self.get_type_display(), self.get_permission_display())
    
    
class Token(models.Model):
    key = models.CharField(max_length=sutil.KEY_SIZE, blank=True)
    secret = models.CharField(max_length=sutil.SECRET_SIZE, blank=True)
    user = models.ForeignKey(User, null=True, blank=True)
    
    ref_provider = models.ManyToManyField(Object, null=True, related_name="provider")
    ref_consumer = models.ManyToManyField(Object, null=True, related_name="consumer")
    allowed_permission = models.SmallIntegerField(choices=sutil.TOKEN_OPERATIONS, default=sutil.TOKEN_OPERATION_REGISTER, null=False)
    status = models.SmallIntegerField(choices=sutil.TOKEN_STATUSS, default=sutil.TOKEN_STATUS_REQUEST, null=False)
    
    time_created = models.DateTimeField(auto_now_add=True)
    time_last = models.DateTimeField(auto_now=True)
    time_validate = models.IntegerField(default=0)
    frequency_min = models.IntegerField(default=0)
    count_used = models.IntegerField(default=0)
    
    def __unicode__(self):
        return u"Token_%s, for %s" % (self.key, self.user)