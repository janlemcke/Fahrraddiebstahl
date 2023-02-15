from django.conf.urls.static import static
from django.urls import path

from data.api import api
from core import settings
from core.views import MainView
from data.views import DataListView

urlpatterns = [
    path("", MainView.as_view(), name="home"),
    path("data", DataListView.as_view(), name="data"),
    path("api/", api.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
