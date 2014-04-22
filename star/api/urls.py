# -*- coding: utf-8 -*-
#    
#    api.urls
#    created by giginet on 2011/09/20
#
from django.conf.urls import url,patterns,include
# from piston.resource import Resource
# from piston.doc import documentation_view

# from handlers import StarHandler
from resources import StarResource
# from tastypie.api import Api
# star_handler = Resource(StarHandler)
# v1_api = Api()
# v1_api.register(StarResource())
star_resource = StarResource()
urlpatterns = patterns('',
    (r'^', include(star_resource.urls)),
)
# urlpatterns = patterns('star',
#     url(r'^(?P<content_type>\d+)/(?P<object_id>\d+)/$',                  'views.adapter', name='star-api'),
#     url(r'^(?P<content_type>\d+)/(?P<object_id>\d+)/(?P<star_id>\d+)/$', 'views.adapter', name='star-api'),
#     # url(r'^doc/$', documentation_view),
# )