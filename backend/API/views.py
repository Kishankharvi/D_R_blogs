from django.shortcuts import render
from django.http import JsonResponse
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.db.models import Sum
# Restframework
from rest_framework import status
from rest_framework.decorators import api_view, APIView
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework_simplejwt.tokens import RefreshToken

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from datetime import datetime

# Others
import json
import random

# Custom Imports
from API import serializers as api_serializer
from API import models as api_models

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class=api_serializer.MyTokenObtainPairSerializer

class RegisterView(generics.CreateAPIView):
    queryset=api_models.User.objects.all()
    permission_classes=[AllowAny]
    serializer_class=api_serializer.RegisterSerializer
class ProfileView(generics.RetrieveUpdateAPIView):
    permission_classes=[AllowAny]
    serializer_class=api_serializer.ProfileSerializer
    def get_object(self):
        user_id=self.kwargs["user_id"]
        user=api_models.User.objects.get(id=user_id)
        profile=api_models.Profile.objects.get(user=user)
        return profile




class CategoryListAPIView(generics.ListAPIView):
        serializer_class=api_serializer.CategorySerializer
        permission_classes=[AllowAny]

        def get_queryset(self):
             return api_models.Category.objects.all()

class PostCategoryListAPIView(generics.ListAPIView):
    serializer_class=api_serializer.PostSerializer
    permission_classes=[AllowAny]

    def get_queryset(self):
        category_slug=self.kwargs["category_slug"]
        category=api_models.Category.objects.get(slug=category_slug)
        return api_models.Post.objects.filter(category=category,status="Active")
    
class PostListAPIView(generics.ListAPIView):
     serializer_class=api_serializer.PostSerializer
     permission_classes=[AllowAny]


     def get_queryset(self):
          return api_models.Post.objects.filter(status="Active")

class PostDetailAPIView(generics.RetrieveAPIView):
    serializer_class=api_serializer.PostSerializer
    permission_classes=[AllowAny]


    def get_object(self):
        slug=self.kwargs["slug"]
        post=api_models.Post.objects.get(slug=slug,status="Active")
        post.view+=1
        post.save()
        return post
    

class LikePostAPIView(APIView):
     @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'user_id': openapi.Schema(type=openapi.TYPE_INTEGER),
                'post_id': openapi.Schema(type=openapi.TYPE_STRING),
            },
        ),
    )
     def post(self,request):
          user_id=request.data["user_id"]
          post_id=request.data["post_id"]

          user=api_models.User.objects.get(id=user_id)

          post=api_models.Post.objects.get(id=post_id)

          if user in post.likes.all():
               post.likes.remove(user)
               return Response({"message":"Post disliked"},status=status.HTTP_200_OK)

          else:
               post.likes.add(user)
            #    api_models.Notification.objects.create(
            #         user=post.user,
            #         post=post,
            #         type="Like"
            #    )
               return Response({"message" :"Post liked"},status=status.HTTP_201_CREATED)
# import logging
# from rest_framework.response import Response
# from rest_framework import status
# from rest_framework.views import APIView
# from drf_yasg import openapi
# from drf_yasg.utils import swagger_auto_schema
# from . import api_models

# logger = logging.getLogger(__name__)

# class PostCommentAPIView(APIView):
#     @swagger_auto_schema(
#         request_body=openapi.Schema(
#             type=openapi.TYPE_OBJECT,
#             required=['post_id', 'name', 'email', 'comment'],
#             properties={
#                 'post_id': openapi.Schema(type=openapi.TYPE_INTEGER),
#                 'name': openapi.Schema(type=openapi.TYPE_STRING),
#                 'email': openapi.Schema(type=openapi.TYPE_STRING, format='email'),
#                 'comment': openapi.Schema(type=openapi.TYPE_STRING),
#             },
#         ),
#     )
#     def post(self, request):
#         try:
#             post_id = request.data["post_id"]
#             name = request.data["name"]
#             email = request.data["email"]
#             comment = request.data["comment"]

#             # Logging for debugging purposes
#             logger.info(f"Attempting to retrieve post with id {post_id}")
#             post = api_models.Post.objects.get(id=post_id)
            
#             logger.info("Creating a new comment")
#             api_models.Comment.objects.create(
#                 post=post,
#                 name=name,
#                 email=email,
#                 comment=comment,
#             )

#             logger.info("Creating a notification")
#             api_models.Notification.objects.create(
#                 user=post.user,
#                 post=post,
#                 type="Comment"
#             )
#             return Response({"message": "Comment sent"}, status=status.HTTP_201_CREATED)
        
#         except api_models.Post.DoesNotExist:
#             logger.error(f"Post with id {post_id} does not exist")
#             return Response({"error": "Post not found"}, status=status.HTTP_404_NOT_FOUND)
#         except KeyError as e:
#             logger.error(f"Missing field in request: {str(e)}")
#             return Response({"error": f"Missing field: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)
#         except Exception as e:
#             logger.exception("An unexpected error occurred")
#             return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)





# from rest_framework.response import Response
# from rest_framework import status
# from rest_framework.views import APIView
# from drf_yasg import openapi
# from drf_yasg.utils import swagger_auto_schema
# from . import api_models  # Update this import based on your project structure

# class PostCommentAPIView(APIView):
#     @swagger_auto_schema(
#         request_body=openapi.Schema(
#             type=openapi.TYPE_OBJECT,
#             required=['post_id', 'name', 'email', 'comment'],
#             properties={
#                 'post_id': openapi.Schema(type=openapi.TYPE_INTEGER),
#                 'name': openapi.Schema(type=openapi.TYPE_STRING),
#                 'email': openapi.Schema(type=openapi.TYPE_STRING, format='email'),
#                 'comment': openapi.Schema(type=openapi.TYPE_STRING),
#             },
#         ),
#     )
#     def post(self, request):
#         try:
#             post_id = request.data["post_id"]
#             name = request.data["name"]
#             email = request.data["email"]
#             comment = request.data["comment"]

#             post = api_models.Post.objects.get(id=post_id)
#             api_models.Comment.objects.create(
#                 post=post,
#                 name=name,
#                 email=email,
#                 comment=comment,
#             )
#             api_models.Notification.objects.create(
#                 user=post.user,
#                 post=post,
#                 type="Comment"
#             )
#             return Response({"message": "Comment sent"}, status=status.HTTP_201_CREATED)
        
#         except api_models.Post.DoesNotExist:
#             return Response({"error": "Post not found"}, status=status.HTTP_404_NOT_FOUND)
#         except KeyError as e:
#             return Response({"error": f"Missing field: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)
#         except Exception as e:
#             return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




class PostCommentAPIView(APIView):
     @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
            
                'post_id': openapi.Schema(type=openapi.TYPE_INTEGER),
                'name': openapi.Schema(type=openapi.TYPE_STRING),
                'email': openapi.Schema(type=openapi.TYPE_STRING),
                'comment': openapi.Schema(type=openapi.TYPE_STRING),
            },
        ),
    )
     def post(self,request):
      
          post_id=request.data["post_id"]
          name=request.data["name"]
          email=request.data["email"]
          comment=request.data["comment"]
         

          post=api_models.Post.objects.get(id=post_id)
          api_models.Comment.objects.create(
          post=post,
          name=name,
          email=email,
          comment=comment,
          )
        #   api_models.Notification.objects.create(
        #             user=post.user,
        #             post=post,
        #             type="Comment"
        #        )
          return Response({"message ":"Comment sent"},status=status.HTTP_201_CREATED)


     

class BookmarkPostAPIView(APIView):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
          properties={
                'user_id': openapi.Schema(type=openapi.TYPE_INTEGER),
                'post_id': openapi.Schema(type=openapi.TYPE_INTEGER),
            },
        ),
    )
    def post(self,request):
        user_id=request.data["user_id"]
        post_id=request.data["post_id"]

        user=api_models.User.objects.get(id=user_id)

        post=api_models.Post.objects.get(id=post_id)
        bookmark=api_models.BookMark.objects.filter(post=post, user=user)

        if bookmark:
            bookmark.delete()
            return Response({"message" :"Post removed from bookmarks"},status=status.HTTP_200_OK)
        else:
            api_models.BookMark.objects.create(post=post, user=user)

            # api_models.Notification.objects.create(
            #         user=post.user,
            #         post=post,
            #         type="BookMark"
            #    )
            return Response({"message":"Post added to bookmarks"},status=status.HTTP_201_CREATED)
        




#dashboard stats


class DashBoardStats(generics.ListAPIView):
     serializer_class=api_serializer.AuthorSerializer
     permission_classes=[AllowAny]

     def get_queryset(self):
          user_id=self.kwargs['user_id']
          user=api_models.User.objects.get(id=user_id)


          views=api_models.Post.objects.filter(user=user).aggregate(view=Sum("view"))["view"]
          comments=api_models.Comment.objects.filter(post__user=user).count()
          posts=api_models.Post.objects.filter(user=user).count()
          likes = api_models.Post.objects.filter(user=user).aggregate(totallikes=Sum("likes"))["totallikes"]

          bookmark=api_models.BookMark.objects.filter(post__user=user)
          return [{
               "views":views,
               "comments":comments,
               "posts":posts,
               "likes":likes,
               "bookmarks":bookmark.count(),
              }]
     def list(self,request,*args,**kwargs):
            queryset=self.get_queryset()
            serializer=self.get_serializer(queryset,many=True)
            return Response(serializer.data)




class DashBoardPostLists(generics.ListAPIView):
    serializer_class=api_serializer.PostSerializer
    permission_classes=[AllowAny]

    def get_queryset(self):
        user_id=self.kwargs["user_id"]

        user=api_models.User.objects.get(id=user_id)
        return api_models.Post.objects.filter(user=user).order_by("-id")

class DashBoardCommentLists(generics.ListAPIView):
    serializer_class=api_serializer.CommentSerializer
    permission_classes=[AllowAny]


    def get_queryset(self):
        user_id=self.kwargs["user_id"]
        user=api_models.User.objects.get(id=user_id)
        return api_models.Comment.objects.filter(post__user=user)

class DashBoardNotificationLists(generics.ListAPIView):
    serializer_class=api_serializer.NotificationSerializer
    permission_classes=[AllowAny]

    def get_queryset(self):
        user_id=self.kwargs["user_id"]
        user=api_models.User.objects.get(id=user_id)
        return api_models.Notification.objects.filter(seen=False,user=user)

class DashBoardMarkNotificationSeen(APIView):
     def post(self,request):
          noti_id=request.data["noti_id"]
          noti=api_models.Notification.objects.get(id=noti_id)
          noti.seen=True
          noti.save()
          return Response({"message": "Notif marked ass seen"},status=status.HTTP_200_OK)
     
class DashBoardReplyCommentAPIView(APIView):
    def post(self, request):
              comment_id=request.data["comment_id"]
              reply=request.data["reply"]
              comment=api_models.Comment.objects.get(id=comment_id)
              comment.reply=reply
              comment.save()
              return Response({"message":"Comment response sent"},status=status.HTTP_201_CREATED)


class DashboardPostCreateAPIView(generics.CreateAPIView):
    serializer_class=api_serializer.PostSerializer
    permission_classes=[AllowAny]

    def create(self,request,*args,**kwargs):
        print(request.data)

        user_id=request.data.get('user_id')
        title=request.data.get('title')
        image=request.data.get('image')
        description=request.data.get('description')
        tags=request.data.get('tags')
        category_id=request.data.get('category')
        post_status=request.data.get('post_status')


        user=api_models.User.objects.get(id=user_id)
        category=api_models.Category.objects.get(id=category_id)
        api_models.Post.objects.create(
            user=user,
            title=title,
            image=image,
            description=description,
            tags=tags,
            category=category,
            post_status=post_status,
        )
        return Response({"message":"Post created successfully"},status=status.HTTP_201_CREATED)

class DashboardPostEditAPIView(generics.RetrieveUpdateDestroyAPIView):
        serializer_class=api_serializer.PostSerializer
        permission_classes=[AllowAny]
        def get_object(self):
          User_id=self.kwargs['user_id']
          Post_id=self.kwargs['post_id']
          user=api_models.User.objects.get(id=User_id)
          return api_models.Post.objects.get(id=User_id,user=user)
        def update(self,request,*args,**kwargs):
             post_instance=self.get_object()
             title=request.get('title')
             image=request.get('image')
             description=request.get('description')
             tags=request.get('tags')
             category_id=request.get('category')
             post_status=request.get('post_status')

             category=api_models.Category.objects.get(id=category_id)

             post_instance.title=title
             if image!='undefined':
                  post_instance.image=image
             post_instance.description=description
             post_instance.tags=tags
             post_instance.category=category
             post_instance.post_status=post_status
             post_instance.save()

             return Response({"message":"Post updated successfully"},status=status.HTTP_200_OK)


