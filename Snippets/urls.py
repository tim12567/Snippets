from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from MainApp import views

urlpatterns = [
    path('', views.index_page, name='home'),
    # path('snippets/add', views.add_snippet_page, name='sp_add'),
    path('snippets/list', views.snippets_page, name='sp_list'),
    path('snippets/my', views.snippets_my, name='sp_my'),
    path('snippet/<int:value>', views.snippet, name='sp_val'),
    path('snippet/<int:value>/edit', views.snippet_edit, name='sp_edit'),
    path('snippet/<int:value>/delete', views.snippet_delete, name='sp_del'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('register', views.create_user, name='register'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)