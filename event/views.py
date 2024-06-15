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
        posts = Event.objects.all().order_by('date')
        paginated_posts = self.pagination_class.paginate_queryset(posts, request)
        serializer = EventSerializer(paginated_posts, many=True)
        return self.pagination_class.get_paginated_response(serializer.data)

class AddEventView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data.copy()
        data['user_id'] = request.user.id
        
        if 'event_image' in request.FILES:
            data['event_image'] = request.FILES['event_image']
        
        serializer = CreateEventSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class DeleteEventView(APIView):
    def delete(self, request, pk):
        try:
            event = Event.objects.get(id=pk)
        except:
            return Response({"Message": "Event not found"}, status=status.HTTP_404_NOT_FOUND)

        if request.user != event.user_id:
            return Response(status=status.HTTP_403_FORBIDDEN)

        event.delete()

        return Response({"Message": "Event deleted successfully"}, status=status.HTTP_204_NO_CONTENT)