from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from API import views as api_views



urlpatterns = [
path("user/token/",api_views.MyTokenObtainPairView.as_view()),
path("user/token/refresh/",TokenRefreshView.as_view()),
path("user/register/",api_views.RegisterView.as_view()),
path("user/profile/<user_id>/",api_views.ProfileView.as_view()),






path("post/category/lists/",api_views.CategoryListAPIView.as_view()),


path("post/category/posts/<category_slug>/",api_views.PostCategoryListAPIView.as_view()),





    path("post/lists/",api_views.PostListAPIView.as_view()),
    path("post/details/<slug>/",api_views.PostDetailAPIView.as_view()),

path("post/like-post/",api_views.LikePostAPIView.as_view())








]