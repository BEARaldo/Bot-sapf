from django.urls import path, include
from . import views, settings
from .services import *
from .views import *


urlpatterns = [
    path('', LoginView.as_view(), name='login_view'),
    path('login/', LoginView.as_view(), name='login_view'),
    path('home/', HomeView.as_view(), name='home'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('choice/', ConsultaCitizenView.as_view(), name='choice'),
    path('consulta_eleitoral/', ConsultaEleitoralView.as_view(), name='consulta_eleitoral'),
    path('accounts/', include('django.contrib.auth.urls')),
]

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