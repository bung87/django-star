# -*- coding: utf-8 -*-
#    
#    api.urls
#    created by giginet on 2014/04/22
#
from django.conf.urls import url,patterns,include

from resources import StarResource
# from tastypie.api import Api
# star_handler = Resource(StarHandler)
# v1_api = Api()
# v1_api.register(StarResource())
star_resource = StarResource()
urlpatterns = patterns('',
    (r'^', include(star_resource.urls)),
)