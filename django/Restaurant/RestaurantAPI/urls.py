from django.urls import path
from . import views
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('menu-items', views.menu_items),
    path('menu-items/', views.menu_items),
    path('menu-items/<int:pk>', views.SingleMenuItemView.as_view()),
    path('menu-items/<int:pk>/', views.SingleMenuItemView.as_view()),
    path('category', views.CategoryView.as_view()),
    path('category/', views.CategoryView.as_view()),
    path('category/<int:pk>', views.SingleCategoryView.as_view()),
    path('category/<int:pk>/', views.SingleCategoryView.as_view()),
    path('secret', views.secret),
    path('secret/', views.secret),
    path('api-token-auth', obtain_auth_token),
    path('api-token-auth/', obtain_auth_token),
    path('manager-view', views.manager_view),
    path('manager-view/', views.manager_view),
    path('throttle-check', views.throttle_check),
    path('throttle-check/', views.throttle_check),
    path('throttle-check-auth', views.throttle_check_auth),
    path('throttle-check-auth/', views.throttle_check_auth),
    path('groups/manager/users', views.managers),
    path('groups/manager/users/', views.managers),
]