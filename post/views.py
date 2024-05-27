from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer

# Create your views here.
class PostView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        posts = Post.objects.all()

        return Response(PostSerializer(posts, many=True).data)

    def post(self, request):
        serializer = PostSerializer(data=request.data)

        if serializer.is_valid():
            post = serializer.create(serializer.validated_data)
            post.save()

            return Response(status=status.HTTP_201_CREATED)

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
        if request.user != Post.objects.get(id=pk).user_id:
            return Response(status=status.HTTP_403_FORBIDDEN)

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

class CommentDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, comment_id):
        try:
            comment = Comment.objects.get(id=comment_id, author=request.user)
        except Comment.DoesNotExist:
            return Response({"error": "Comment not found or not authorized"}, status=status.HTTP_404_NOT_FOUND)
        
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
