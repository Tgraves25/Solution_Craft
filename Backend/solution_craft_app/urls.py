from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', views.api_root),
    path('signup/', views.SignupView.as_view(), name='signup'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('tickets/', views.TicketAPIView.as_view(), name='ticket_list_create'),
    path('tickets/<int:pk>/', views.TicketDetailAPIView.as_view(), name='ticket_detail'),
    path('ai_recommendation/', views.ai_recommendation, name='ai_recommendation'),
]

