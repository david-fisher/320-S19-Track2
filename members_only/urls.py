from django.urls import path, include
from django.contrib import admin
from rest_framework import routers

admin.autodiscover()

import members_only.views

# To add a new path, first import the app:
# import blog
#
# Then add the new path:
# path('blog/', blog.urls, name="blog")
#
# Learn more here: https://docs.djangoproject.com/en/2.1/topics/http/urls/

router = routers.DefaultRouter()
router.register(r'users', members_only.views.UserViewSet)
router.register(r'groups', members_only.views.GroupViewSet)

urlpatterns = [
    path("", members_only.views.index, name="index"),
    path('api/', include(router.urls)),
    path("db/", members_only.views.db, name="db"),
    path("admin/", admin.site.urls),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
