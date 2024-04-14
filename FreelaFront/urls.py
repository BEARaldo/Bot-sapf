from django.urls import path, include
from . import views, settings


urlpatterns = [
    path('',views.login_view, name='login_view'),
    #pagina1 é o mesmo html da rota login/
    path('pagina1/', views.pagina1, name="pagina1"),
    path('accounts/', include('django.contrib.auth.urls')),
    #testes abaixo:
    path('choice/', views.choice, name='choice'),
    #path('test/', views.test, name='test'),

    path('reg/', views.reg, name='reg'),
    path('return_cpf/', views.return_cpf, name='test')


]
if settings.DEBUG:
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    urlpatterns += staticfiles_urlpatterns()