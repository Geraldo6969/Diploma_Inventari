from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import path
from django.views.generic import RedirectView
from magazina import views
from django.conf import settings
from django.conf.urls.static import static
from magazina.views import RememberMeLoginView, lista_produkteve




urlpatterns = [
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(pattern_name='login', permanent=False), name='root'),
    path('login/', RememberMeLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('produkte/', lista_produkteve, name='home'),
    path('produkte/shto/', views.shto_produkt, name='shto_produkt'),
    path('raportet/', views.raportet, name='raportet'),
    path('importo-excel/', views.importo_excel, name='importo_excel'),
    path('skaner/', views.skaner, name='skaner'),
    # 4. Faqja ku shfaqet QR kodi i një produkti specifik (për ta printuar/shfaqur)
    path('produkti/<int:produkt_id>/qr/', views.gjenero_qr, name='gjenero_qr'),

    # 5. Faqja e menaxhimit (Shto/Hiq sasi) që hapet PAS skanimit
    path('produkti/<int:produkt_id>/menaxho/', views.menaxho_produktin, name='menaxho_produktin'),
    path('produkti/<int:produkt_id>/dashboard/', views.dashboard_produkti, name='dashboard_produkti'),
    # Shto këtë rresht te urlpatterns (sigurohu që name është 'modifiko_produktin')
    path('produkti/<int:produkt_id>/modifiko/', views.modifiko_produktin, name='modifiko_produktin'),
    path('raportet/excel/', views.eksporto_excel, name='eksporto_excel'),
    path('raportet/word/', views.eksporto_word, name='eksporto_word'),
   
] 

# KJO PJESË ËSHTË E DETYRUESHME:
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


# Ndryshimi i teksteve zyrtare të Panelit të Adminit
admin.site.site_header = "E Inventory"
admin.site.site_title = "E Inventory"
admin.site.index_title = "E Inventory"
