# -*- coding: utf-8 -*-
#    
#    api.handlers
#    created by giginet on 2011/09/20
#
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.contenttypes.models import ContentType
from tastypie.resources import Resource,ModelResource
from ..models import Star
from django.conf.urls import url
class StarResource(ModelResource):
    class Meta:
        resource_name = 'star'
        queryset=Star.objects.all()
        allowed_method = ('GET', 'POST', 'DELETE',)
        # detail_uri_name = 'object_id'
    def prepend_urls(self):
        return [
            url(r"^(?P<content_type>\d+)/(?P<object_id>\d+)/$" , self.wrap_view('dispatch_detail'), name="star-api"),
            url(r"^%s/(?P<content_type>\d+)/(?P<object_id>\d+)/$" % self._meta.resource_name, self.wrap_view('dispatch_detail')),
            # url(r'^(?P<content_type>\d+)/(?P<object_id>\d+)/(?P<star_id>\d+)/$', v1_api.top_level, name='star-api')
        ]
    def dispatch(self, request_type, request, **kwargs):
        content_type_id = kwargs.pop('content_type')
        object_id = kwargs['object_id']
        content_type = get_object_or_404(ContentType, pk=content_type_id)
        kwargs['content_type']=content_type
        print kwargs
        return super(StarResource, self).dispatch(request_type, request, **kwargs)
# def get_or_not_found(fn):
#     """Get and set object or return rc.NOT_FOUND decorator
#        Get object instance from content_type and object_id and set it to request.obj
#        and call decorated function, or return rc.NOT_FOUND when object could not be found
#        this snippet is quoted from 'hhny ^/ttps://github.com/lambdalisue/django-universaltag/blob/master/universaltag/api/handlers.py#L45'.
#     """
#     def wrapper(self, bundle, content_type, object_id, *args, **kwargs):
#         try:
#             ctype = get_object_or_404(ContentType, pk=content_type)
#             obj = ctype.get_object_for_this_type(pk=object_id)
#             bundle.obj = obj
#             return fn(self, bundle, content_type, object_id, *args, **kwargs)
#         except (Http404, ObjectDoesNotExist):
#             pass
#             # return rc.NOT_FOUND
#     return wrapper
#
# class StarResource(Resource):
#
#     class Meta:
#         # queryset = Star.objects.all()
#         resource_name = 'star'
#         object_class = Star
#         allowed_method = ('GET', 'POST', 'DELETE',)
#     # def prepend_urls(self):
#     #     return urlpatterns
#
#
#     # fields = (
#     #           'pk',
#     #           'type',
#     #           ('author', ('username', 'pk', ), ),
#     #           'comment'
#     # )
#     @get_or_not_found
#     def obj_get(self, bundle, **kwargs):
#         bucket = self._bucket()
#         instance = bucket.get_for_object(bundle.obj)
#         from django.forms.models import model_to_dict
#         return model_to_dict(instance)
#     @get_or_not_found
#     def read(self, request, content_type, object_id):
#         qs = self.model.objects.get_for_object(request.obj)
#         return qs
#
#     @get_or_not_found
#     def create(self, request, content_type, object_id):
#         comment = request.POST.get('comment', '');
#         tag = request.POST.get('tag', '');
#         if request.user.is_authenticated():
#             instance = self.model.objects.add_for_object(request.obj, request.user, comment, tag)
#             return instance
#         return rc.FORBIDDEN
#
#     def delete(self, request, content_type, object_id, star_id):
#         if not star_id: rc.BAD_REQUEST
#         star = self.model.objects.get(pk=star_id)
#         if request.user.is_authenticated() and request.user.pk is star.author.pk:
#             star.delete()
#             return rc.DELETED
#         return rc.FORBIDDEN