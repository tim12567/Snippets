from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from MainApp import views

urlpatterns = [
    path('', views.index_page, name='home'),
    path('snippets/add', views.add_snippet_page, name='sp_add'),
    path('snippets/list', views.snippets_page, name='sp_list'),
    path('snippet/<int:value>', views.snippet, name='sp_val'),
    path('snippet/create', views.create_snippet, name='create_snippet_st'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)