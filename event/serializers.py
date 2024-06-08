from rest_framework.serializers import ModelSerializer
from .models import Event
from misc.serializers import ImageSerializer

class EventSerializer(ModelSerializer):
    event_image = ImageSerializer()
    
    class Meta:
        model = Event
        fields = ('title', 'date', 'description', 'user_id', 'event_image', 'event_categories', 'event_tags')
        # read_only_fields = ['user']

class CreateEventSerializer(ModelSerializer):
    
    class Meta:
        model = Event
        fields = ('title', 'date', 'description', 'user_id', 'event_image', 'event_categories', 'event_tags')