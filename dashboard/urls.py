from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.DashboardView.as_view(), name='home'),

    # Login/Logout
    path('accounts/login/', views.LoginPageView.as_view(), name='login'),
    path('accounts/logout/',views.LogoutView.as_view(), name='logout'),

    # Server Type Crud
    path('server-types/', views.ServerTypeListView.as_view(), name='server-type-list'),
    path('server-type/create', views.ServerTypeCreateView.as_view(), name='server-type-create'),
    path('server-type/<int:pk>/update', views.ServerTypeUpdateView.as_view(), name='server-type-update'),
    path('server-type/<int:pk>/delete', views.ServerTypeDeleteView.as_view(), name='server-type-delete'),

    # Disk Type Crud
    path('disk-types/', views.DiskTypeListView.as_view(), name='disk-type-list'),
    path('disk-type/create', views.DiskTypeCreateView.as_view(), name='disk-type-create'),
    path('disk-type/<int:pk>/update', views.DiskTypeUpdateView.as_view(), name='disk-type-update'),
    path('disk-type/<int:pk>/delete', views.DiskTypeDeleteView.as_view(), name='disk-type-delete'),

    # Server Owner Crud
    path('server-owners/', views.ServerOwnerListView.as_view(), name='server-owner-list'),
    path('server-owner/create', views.ServerOwnerCreateView.as_view(), name='server-owner-create'),
    path('server-owner/<int:pk>/update', views.ServerOwnerUpdateView.as_view(), name='server-owner-update'),
    path('server-owner/<int:pk>/delete', views.ServerOwnerDeleteView.as_view(), name='server-owner-delete'),

    # Server Location Crud
    path('server-locations/', views.ServerLocationListView.as_view(), name='server-location-list'),
    path('server-locations/create', views.ServerLocationCreateView.as_view(), name='server-location-create'),
    path('server-locations/<int:pk>/update', views.ServerLocationUpdateView.as_view(), name='server-location-update'),
    path('server-locations/<int:pk>/delete', views.ServerLocationDeleteView.as_view(), name='server-location-delete'),

    # Server Crud
    path('servers/', views.ServerListView.as_view(), name='server-list'),
    path('server/create', views.ServerCreateView.as_view(), name='server-create'),
    path('server/<int:pk>/detail', views.ServerDetailView.as_view(), name='server-detail'),
    path('server/<int:pk>/update', views.ServerUpdateView.as_view(), name='server-update'),
    path('server/<int:pk>/delete', views.ServerDeleteView.as_view(), name='server-delete'),

    # Server Pdf
    path('server/pdf/create', views.ServerPDFGeneratorView.as_view(), name='server-pdf-create'),
    path('server/pdf/email', views.ServerPDFMailView.as_view(), name='server-pdf-email'),


    # User CRUD
    path('users/', views.UserListView.as_view(), name='user-list'),
    path('user/create', views.UserCreateView.as_view(), name='user-create'),
    path('user/<int:pk>/update', views.UserUpdateView.as_view(), name='user-update'),
    path('user/<int:pk>/status', views.UserStatusView.as_view(), name='user-status'),
    path('user/<int:pk>/password-reset', views.UserPasswordResetView.as_view(), name='user-password-reset'),


]