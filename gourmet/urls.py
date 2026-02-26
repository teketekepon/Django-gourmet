from django.contrib import admin
from django.urls import include, path
from django.urls.resolvers import URLPattern, URLResolver
from django.conf import settings
from django.conf.urls.static import static

urlpatterns: list[URLPattern | URLResolver] = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('accounts.api_urls')),
    path('api/', include('dish.api_urls')),
]

if settings.DEBUG:
    urlpatterns += static(
      # MEDIA_URL = '/media/'
      settings.MEDIA_URL,
      # MEDIA_ROOTにリダイレクト
      document_root=settings.MEDIA_ROOT
      )


