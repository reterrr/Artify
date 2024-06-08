from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Event
from .serializers import EventSerializer, CreateEventSerializer
from rest_framework.pagination import PageNumberPagination

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100
    
# Create your views here.
class EventView(APIView):
    pagination_class = StandardResultsSetPagination()

    def get(self, request):
        posts = Event.objects.all().order_by('-date')
        paginated_posts = self.pagination_class.paginate_queryset(posts, request)
        serializer = EventSerializer(paginated_posts, many=True)
        return self.pagination_class.get_paginated_response(serializer.data)

class AddEventView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data.copy()
        data['user_id'] = request.user.id
        serializer = CreateEventSerializer(data=data)
        if serializer.is_valid():
            serializer.save(user_id=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)