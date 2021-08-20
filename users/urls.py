from django.urls import path, include
from users import views
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register('register', views.UserRegisterViewSet)

urlpatterns = [
    path('login/', views.UserLoginApiView.as_view()),
    path('', include(router.urls))
]
