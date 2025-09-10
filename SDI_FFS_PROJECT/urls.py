from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),
    path('master/', include('masters.urls')),
    path('bi/', include('business_intelligence.urls')),
    path('acr/', include('accounting_report.urls')),
    path('operations/', include('operations.urls')),
    path('crm/', include('crm.urls')),
    path('hr/', include('hr.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('api/v1/', include('api.urls')),
    path('accounting/', include('accounting.urls')),
    re_path(r'^ckeditor/', include('ckeditor_uploader.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# ✅ Add debug toolbar only in DEBUG mode
if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]
