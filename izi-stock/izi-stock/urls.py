
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('users.urls')),
    path('', include('products.urls')),

]

urlpatterns += staticfiles_urlpatterns()


# gestion des fichiers statiques
if settings.DEBUG:
    urlpatterns += static(
        settings.STATIC_URL,
        document_root=settings.STATIC_ROOT
    )+static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )