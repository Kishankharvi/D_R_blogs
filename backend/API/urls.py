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

path("post/like-post/",api_views.LikePostAPIView.as_view()),
path("post/comment-post/",api_views.PostCommentAPIView.as_view()),


path("post/bookmark-post/",api_views.BookmarkPostAPIView.as_view()),




#dashboard
path("author/dashboard/stats/<user_id>/",api_views.DashBoardStats.as_view()),

path("author/dashboard/comment-list/<user_id>/",api_views.DashBoardCommentLists.as_view()),
path("author/dashboard/reply-comment/",api_views.DashBoardReplyCommentAPIView.as_view()),
path("author/dashboard/noti-list/<user_id>/",api_views.DashBoardNotificationLists.as_view()),
path("author/dashboard/noti-mark-seen/",api_views.DashBoardMarkNotificationSeen.as_view()),


]
{
    "noti_id": 1
}
