# -*- coding: utf-8 -*-
#    
#    api.resource
#    created by bung on 2014/04/22
#

from django.shortcuts import get_object_or_404
from django.contrib.contenttypes.models import ContentType
from tastypie.constants import ALL,ALL_WITH_RELATIONS
from ..models import Star
from django.conf.urls import url
import urlparse
from tastypie.serializers import Serializer
from tastypie.authorization import DjangoAuthorization
from tastypie.resources import ModelResource
from tastypie import fields
from django.contrib.auth.models import User

class UserResource(ModelResource):

    class Meta:
        queryset = User.objects.all()
        resource_name = 'auth/user'
        excludes = ['is_active','first_name','date_joined','email', 'password', 'is_superuser','is_staff','last_login','last_name']
        include_resource_uri = False
        serializer = Serializer(formats=['json', 'plist'])
class urlencodeSerializer(Serializer):
    formats = ['json', 'jsonp', 'xml', 'yaml', 'html', 'plist', 'urlencode']
    content_types = {
        'json': 'application/json',
        'jsonp': 'text/javascript',
        'xml': 'application/xml',
        'yaml': 'text/yaml',
        'html': 'text/html',
        'plist': 'application/x-plist',
        'urlencode': 'application/x-www-form-urlencoded',
        }
    def from_urlencode(self, data,options=None):
        """ handles basic formencoded url posts """
        qs = dict((k, v if len(v)>1 else v[0] )
            for k, v in urlparse.parse_qs(data).iteritems())
        return qs

    def to_urlencode(self,content):
        pass

class StarResource(ModelResource):
    author = fields.ForeignKey(UserResource, 'author',full=True)
    class Meta:
        resource_name = 'star'
        queryset=Star.objects.all()
        allowed_method = ('GET', 'POST', 'DELETE',)
        authorization = DjangoAuthorization()
        filtering = {"author": ALL_WITH_RELATIONS }
        include_resource_uri = False
        always_return_data = True
        excludes = ['object_id', 'id', 'comment','resource_uri','tag','created_at']
        serializer = urlencodeSerializer()
    def alter_list_data_to_serialize(self, request, data_dict):
        import copy
        if isinstance(data_dict, dict):
            if 'meta' in data_dict:
                del(data_dict['meta'])
                data_dict['objects'] = copy.copy(data_dict['objects'])

        return data_dict
    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/(?P<content_type>\d+)/(?P<object_id>\d+)/$" % self._meta.resource_name, self.wrap_view('dispatch_list'),name="star-api"),
            url(r'^(?P<resource_name>%s)/(?P<content_type>\d+)/(?P<object_id>\d+)/(?P<star_id>\d+)/$'% self._meta.resource_name,self.wrap_view('dispatch_list'), name='star-api')
        ]

    def obj_create(self, bundle, **kwargs):
        kwargs['comment']=bundle.request.POST['comment']
        kwargs['author']=bundle.request.user
        return super(StarResource, self).obj_create(bundle, **kwargs)
    def obj_delete(self, bundle, **kwargs):
        kwargs['author']=bundle.request.user
        kwargs['id'] = kwargs['star_id']
        return super(StarResource, self).obj_delete(bundle, **kwargs)
    def dispatch(self, request_type, request, **kwargs):
        content_type_id = kwargs.pop('content_type')
        content_type = get_object_or_404(ContentType, pk=content_type_id)
        kwargs['content_type']=content_type
        return super(StarResource, self).dispatch(request_type, request, **kwargs)

#             return rc.DELETED
#         return rc.FORBIDDEN