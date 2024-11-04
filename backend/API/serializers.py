from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers

from API import models as  API_models

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["full_name"] = user.full_name
        
        return token
    
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True,validators=[validate_password])

    password2= serializers.CharField(write_only=True, required=True)
    class Meta:
        model=API_models.User
        fields=('email','password','password2','full_name')
    def validate(self,attr):
        if attr['password'] != attr['password2']:
            raise serializers.ValidationError("Passwords must match.")
        return attr
    def create(self,validated_data):
        user=API_models.User.objects.create(

            full_name=validated_data['full_name'],
            email=validated_data['email'],
        
        )
        email_username,mobile=user.email.split("@")
        user.username=email_username
        user.set_password(validated_data['password'])
        user.save() 
        return user
    
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=API_models.User
        fields="__all__"
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model=API_models.Profile
        fields="__all__"
        
class CategorySerializer(serializers.ModelSerializer):
    def get_post_count(self, category):
        return category.post_count()
    



    class Meta:
        model=API_models.Category
        fields=["id", "title","image", "slug","post_count", ]

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model=API_models.Comment
        fields="__all__"
    def __init__(self, *args, **kwargs):
        super(CommentSerializer, self).__init__(*args, **kwargs
        )
        request =self.context.get('request')
        if request and request.method == 'POST':
            self.Meta.depth=0
        else:
                self.Meta.depth=1

class PostSerializer(serializers.ModelSerializer):
    comments=CommentSerializer(many=True)
    class Meta:
        model=API_models.Post
        fields="__all__"
    def __init__(self, *args, **kwargs):
        super(PostSerializer, self).__init__(*args, **kwargs
        )
        request =self.context.get('request')
        if request and request.method == 'POST':
            self.Meta.depth=0
        else:
                self.Meta.depth=1
                
class BookmarkSerializer(serializers.ModelSerializer):
    class Meta:
        model=API_models.BookMark
        fields="__all__"
    def __init__(self, *args, **kwargs):
        super(BookmarkSerializer, self).__init__(*args, **kwargs
        )
        request =self.context.get('request')
        if request and request.method == 'POST':
            self.Meta.depth=0
        else:
                self.Meta.depth=1
                


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model=API_models.Notification
        fields="__all__"
    def __init__(self, *args, **kwargs):
        super(NotificationSerializer, self).__init__(*args, **kwargs
        )
        request =self.context.get('request')
        if request and request.method == 'POST':
            self.Meta.depth=0
        else:
                self.Meta.depth=1
                
class AuthorSerializer(serializers.Serializer):
    views=serializers.IntegerField(default=0)
    posts=serializers.IntegerField(default=0)

    likes=serializers.IntegerField(default=0)

    bookmarks=serializers.IntegerField(default=0)

    
    
