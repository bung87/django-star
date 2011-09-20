# -*- coding : utf-8 -*-
__author__  = 'giginet <giginet.net@gmail.com>'
__version__ = '1.0.0'
__date__    = '2011/9/20'

from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.generic import GenericForeignKey

class StarManager(models.Manager):
    def get_for_object(self, obj):
        u"""Return stars related to the 'obj.'"""
        ct = ContentType.objects.get_for_model(obj)
        return self.filter(content_type=ct, object_id=obj.pk)
        
    def add_for_object(self, obj, author, comment=""):
        u"""Add a star to 'obj' and return Star instance."""
        ct = ContentType.objects.get_for_model(obj)
        star, created = self.create(author=author, comment=comment, content_type=ct, object_id=obj.pk)
        if created:
            return star
     
    def cleanup_object(self, obj):
        u"""remove all related stars from 'obj'."""
        stars = self.get_for_object(obj)
        for star in stars:
            star.remove()
    
class Star(models.Model):
    u"""model for star"""
    
    content_type    = models.ForeignKey(ContentType, verbose_name=_('content type'), related_name="content_type_set_for_%(class)s")
    object_id       = models.PositiveIntegerField(_('object ID'))
    content_object = GenericForeignKey(ct_field="content_type", fk_field="object_id")
    
    author          = models.ForeignKey(User, verbose_name=_('author'))
    comment         = models.CharField(_('comment'))
    
    created_at      = models.DateTimeField(_('created at'), auto_now=True)
    objects         = StarManager()
    
    class Meta:
        ordering            = ('author.pk',)
        verbose_name        = _('star')
        verbose_name_plural = _('stars')
        
    def __unicode__(self):
        return self.content_object.__unicode__()