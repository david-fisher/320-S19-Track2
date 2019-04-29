from django.urls import path, include
from django.contrib import admin
from rest_framework import routers
from rest_framework.authtoken import views

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
router.register(r'user', members_only.views.UserViewSet)
router.register(r'post', members_only.views.PostViewSet)
router.register(r'comment', members_only.views.CommentViewSet)
router.register(r'photo', members_only.views.ImageViewSet)
router.register(r'short-link', members_only.views.ShortLinkViewSet)

urlpatterns = [
    path("", members_only.views.index, name="index"),
    path("feed/", members_only.views.index, name="index"),
    path("user/login", members_only.views.index, name="index"),
    path("user/logout", members_only.views.index, name="index"),
    path("user/invite", members_only.views.index, name="index"),
    path("user/setup", members_only.views.index, name="index"),
    path('api/', include(router.urls)),
    path("admin/", admin.site.urls),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api-token-auth/', views.obtain_auth_token),
]
