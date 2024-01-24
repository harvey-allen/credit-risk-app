from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularSwaggerView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("calculate/", include("calculate.urls")),
    path("", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger"),
]
