"""petpal URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static
from django.conf import settings
from django.conf.urls import include, url  # For django versions before 2.0
from django.urls import include, path  # For django versions from 2.0 and up
from core import views

urlpatterns = [
    path('admin/', admin.site.urls),
]

urlpatterns += [
    path('', RedirectView.as_view(url='dashboard/')),
    path('dashboard/', views.index, name='home'),
    path('pet/<int:pk>', views.pet_detail, name='pet-detail'),
    url(r'^accounts/', include('registration.backends.simple.urls')),
    path('update/', views.profile, name='update-profile'),
    path('addchecklist/<int:pk>', views.add_checklist, name='add-checklist'),
    path('add_pet/', views.add_pet, name='add-pet'),


]

# Use static() to add url mapping to serve static files during development (only)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),

        # For django versions before 2.0:
        # url(r'^__debug__/', include(debug_toolbar.urls)),

    ] + urlpatterns