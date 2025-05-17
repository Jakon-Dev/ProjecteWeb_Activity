from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', auth_views.LoginView.as_view(template_name='auth/login.html'), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register, name='register'),
    path('agents/', views.agents, name='agents'),
    path('agents/roles/', views.agent_roles, name='agent_roles'),
    path('agents/role/<str:role_id>/', views.role_agents, name='role_agents'),
    path('agents/detail/<str:agent_id>/', views.agent_detail, name='agent_detail'),
    path('agents/comment/<str:agent_id>/', views.add_agent_comment, name='add_agent_comment'),
    path('agents/comment/edit/<int:comment_id>/', views.edit_agent_comment, name='edit_agent_comment'),
    path('agents/comment/delete/<int:comment_id>/', views.delete_agent_comment, name='delete_agent_comment'),
    path('maps/', views.maps, name='maps'),
    path('maps/<str:map_id>/', views.map_detail, name='map_detail'),
    path('maps/comment/<str:map_id>/', views.add_map_comment, name='add_map_comment'),
    path('maps/comment/edit/<int:comment_id>/', views.edit_map_comment, name='edit_map_comment'),
    path('maps/comment/delete/<int:comment_id>/', views.delete_map_comment, name='delete_map_comment'),
] 