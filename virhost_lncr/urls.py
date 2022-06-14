from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('ciods.urls')),
    path('Virhostlncr/',include('lncrna.urls',namespace ='lncrna')),
    path('proteomeanalysis/',include('proteome.urls',namespace='proteome')),
    path('contact/',include('contact.urls')),
    path('accounts/', include('accounts.urls', namespace='users')),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
