# recommendation_system/urls.py
from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('matchmaking/', include('matchmaking.urls')),
    path('', RedirectView.as_view(url='/matchmaking/', permanent=True)),  # Redirect to matchmaking app
]
