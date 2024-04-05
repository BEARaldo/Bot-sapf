from django.contrib import admin
from django.urls import path, include
from . import views, settings


urlpatterns = [
    path("admin/", admin.site.urls),
    path('login/',views.login_view, name='login_view'),
    path ('', views.home, name="home"),
    path('pagina1/', views.pagina1, name="pagina1"),
    path('accounts/', include('django.contrib.auth.urls')),
    #testes abaixo:
    path('choice/', views.choice, name='choice'),
    path('test/', views.test, name='test'),

    path('reg/', views.reg, name='reg')


]
if settings.DEBUG:
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    urlpatterns += staticfiles_urlpatterns()