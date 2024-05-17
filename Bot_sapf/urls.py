from django.urls import path, include
from . import views, settings
from .services import *
from .views import *
from django.conf import settings
from django.conf.urls.static import static



from django.contrib import admin

urlpatterns = [
    path('', LoginView.as_view(), name='login_view'),
     path('cadastrar/', CadastrarView.as_view(), name='cadastrar_url'),
    path('consultar_cpf/', ConsultaCitizenView.as_view(), name='consultar_cpf'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('consulta_eleitoral/', ConsultaEleitoralView.as_view(), name='consulta_eleitoral'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('pdfs/<path:filename>', views.ServePDF.as_view(), name='serve_pdf'),


    path('admin/', admin.site.urls),
]
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    urlpatterns += staticfiles_urlpatterns()