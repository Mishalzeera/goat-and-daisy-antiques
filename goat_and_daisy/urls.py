from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
import os 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('profiles/', include('django.contrib.auth.urls')),
    path('profiles/', include('profiles.urls')),
    path('', include('site_layout.urls')),
    path('shop/', include('shop.urls')),
    path('workshop/', include('repairs_restorals.urls')),
    path('invoices/', include('invoices.urls')),
]

admin.site.site_header = "Goat and Daisy"
admin.site.index_title = "Antique Shop and Repairs Admin Panel"

if not "USE_AWS" in os.environ:
    if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                            document_root=settings.MEDIA_ROOT)
