from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Post, Comment, Like
from .serializers import PostSerializer, CommentSerializer, LikeSerializer, CreatePostSerializer, CreateCommentSerializer
from user.models import User
from rest_framework.decorators import permission_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.parsers import MultiPartParser, FormParser

# Create your views here.
class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class UserCommentsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        
        comments = Comment.objects.filter(user_id=user.id)
        comments_data = list(comments.values('id', 'post_id', 'contents', 'publish_date'))

        user_data = {
            'id': user.id,
            'email': user.email,
            'name': user.name,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'bio': user.bio,
            'phone': user.phone,
            'profile_image': user.profile_image.file.url if user.profile_image else None,
            'is_active': user.is_active,
            'is_admin': user.is_admin,
            'created_at': user.created_at,
            'updated_at': user.updated_at
        }
        return JsonResponse({'user': user_data, 'comments': comments_data}, safe=False)

class CommentDeleteView(APIView):
    print("huj")
    def delete(self, request, comment_id):
        try:
            comment = Comment.objects.get(id=comment_id)
        except Comment.DoesNotExist:
            return Response({"Message": "Comment not found"}, status=status.HTTP_404_NOT_FOUND)
        if request.user.id != comment.user_id.id:
            return Response(status=status.HTTP_403_FORBIDDEN)

        comment.delete()

        return Response({"Message": "Comment deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

class PostCommentsView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        
        comments = Comment.objects.filter(post_id=post.id)
        
        return Response(CommentSerializer(comments, many=True).data)

# class PostView(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request, *args, **kwargs):
#         keyword = request.GET.get('keyword', '')
#         if keyword:
#             posts = Post.objects.filter(title__icontains=keyword) | Post.objects.filter(description__icontains=keyword)
#         else:
#             posts = Post.objects.all().order_by('-publish_date')
#             return Response(PostSerializer(posts, many=True).data)

#         serializer = PostSerializer(posts, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)

class PostView(APIView):
    pagination_class = StandardResultsSetPagination()

    def get(self, request):
        keyword = request.query_params.get('keyword', None)
        page = request.query_params.get('page', None)
        
        if keyword:
            posts = Post.objects.filter(title__icontains=keyword).order_by('-publish_date') | Post.objects.filter(description__icontains=keyword).order_by('-publish_date')
        else:
            posts = Post.objects.all().order_by('-publish_date')
        
        if page:
            paginated_posts = self.pagination_class.paginate_queryset(posts, request)
            serializer = PostSerializer(paginated_posts, many=True)
            return self.pagination_class.get_paginated_response(serializer.data)
        else:
            serializer = PostSerializer(posts, many=True)
            return Response(serializer.data)

class CreatePostView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request):
        serializer = CreatePostSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            post = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print(serializer.errors)  # Debugowanie błędów walidacji
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DeletePostView(APIView):
    def delete(self, request, pk):
        try:
            post = Post.objects.get(id=pk)
        except:
            return Response({"Message": "Post not found"}, status=status.HTTP_404_NOT_FOUND)

        if request.user != post.user_id:
            return Response(status=status.HTTP_403_FORBIDDEN)

        post.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)

class FindPostView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, pk):
        # if request.user != Post.objects.get(id=pk).user_id:
            # return Response(status=status.HTTP_403_FORBIDDEN)

        try:
            post = Post.objects.get(id=pk)

        except:
            return Response({"Message": "Post not found"}, status=status.HTTP_404_NOT_FOUND)

        return Response(PostSerializer(post).data)

class CommentCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, post_id):
        post = Post.objects.get(id=post_id)
        data = request.data.copy()
        data['author'] = request.user.id
        data['post'] = post.id
        serializer = CommentSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CreateLikeView(APIView):
    def post(self, request):
        serializer = LikeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PostLikesView(APIView):
    permission_classes = [AllowAny]
    def get(self, request, post_id):
        likes = Like.objects.filter(post_id=post_id)
        liked_users = [
            {
                'id': like.user_id.id,
                'email': like.user_id.email,
                'name': like.user_id.name,
                'first_name': like.user_id.first_name,
                'last_name': like.user_id.last_name
            }
            for like in likes
        ]
        return JsonResponse({'liked_users': liked_users}, safe=False)

class LikeView(APIView):
    def get(self, request, post_id, user_id):
        like = get_object_or_404(Like, post_id=post_id, user_id=user_id)
        serializer = LikeSerializer(like)
        return Response(serializer.data, status=status.HTTP_200_OK)

class DeleteLikeView(APIView):
    def delete(self, request, post_id, user_id):
        try:
            like = get_object_or_404(Like, post_id=post_id, user_id=user_id)
        except:
            return Response({"Message": "Post not found"}, status=status.HTTP_404_NOT_FOUND)

        if request.user != like.user_id:
            return Response(status=status.HTTP_403_FORBIDDEN)

        like.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)

class CommentView(APIView):
    def post(self, request):
        serializer = CreateCommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

