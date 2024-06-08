from django.http.response import JsonResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from post.models import Post
from post.serializers import PostSerializer
from event.models import Event
from event.serializers import EventSerializer
from .serializers import UserSerializer
from rest_framework.exceptions import NotFound
from rest_framework.permissions import AllowAny
from rest_framework import status
from django.shortcuts import get_object_or_404
from misc.models import Image

from .models import User

# Create your views here.

class UpdateUserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        data = request.data.copy()

        # Obsługa pola profile_image
        if 'profile_image' in request.FILES:
            image = Image.objects.create(file=request.FILES['profile_image'])
            user.profile_image = image

        serializer = UserSerializer(user, data=data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            user.save()  # Upewnij się, że zapisujesz użytkownika po przypisaniu obrazu
            return Response({'status': 'success', 'data': serializer.data}, status=status.HTTP_200_OK)
        
        return Response({'status': 'error', 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class UserPostView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        posts = Post.objects.filter(user_id=request.user.id).order_by('-publish_date')
        serializer = PostSerializer(posts, many=True)

        return Response({'posts': serializer.data})

class OwnUserDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data)
    
class UserDetailByIdView(APIView):
    permission_classes = [AllowAny]
    def get(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise NotFound("User not found")

        serializer = UserSerializer(user)
        return Response(serializer.data)
    
class UserPostByIdView(APIView):
    permission_classes = [AllowAny]
    def get(self, request, user_id):
        posts = Post.objects.filter(user_id=user_id)
        serializer = PostSerializer(posts, many=True)

        return Response({'posts': serializer.data})
    
class UserEventsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        events = Event.objects.filter(user_id=user)
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class UserEventsByIdView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        events = Event.objects.filter(user_id=user)
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)