from django.urls import path, include
from . import views, settings
from .services import *
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', LoginView.as_view(), name='login_view'),
    path('consultar_cpf/', ConsultaCitizenView.as_view(), name='consultar_cpf'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('consulta_eleitoral/', ConsultaEleitoralView.as_view(), name='consulta_eleitoral'),
    path('accounts/', include('django.contrib.auth.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
"""  
urlpatterns = [
    path('',views.login_view, name='login_view'),
    #pagina1 é o mesmo html da rota login/
    path('pagina1/', views.pagina1, name="pagina1"),
    path('accounts/', include('django.contrib.auth.urls')),
    #testes abaixo:
    path('choice/', views.consulta_cidadão, name='choice'),
    #path('test/', views.test, name='test'),

    path('reg/', views.reg, name='reg'),
    path('/return_cpf', views.return_cpf, name='test'),
    path('consulta_eleitoral/', ConsultaEleitoralView.as_view(), name='consulta_eleitoral')


]
"""
if settings.DEBUG:
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    urlpatterns += staticfiles_urlpatterns()