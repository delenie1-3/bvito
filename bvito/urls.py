from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.contrib.staticfiles.views import serve

from django.views.decorators.cache import never_cache
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),#маршрут к приложению bvito(корневой)
]

if settings.DEBUG:
    urlpatterns.append(path('static/<path:path>',never_cache(serve)))
    #файлы сайта не кешируются / ПОКА НЕ ПОНЯТНАЯ ОШИБКА
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)