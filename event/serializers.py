from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from .models import Event
from misc.serializers import ImageSerializer
from misc.models import Image

class EventSerializer(ModelSerializer):
    event_image = ImageSerializer()
    
    class Meta:
        model = Event
        fields = ('id', 'title', 'date', 'description', 'user_id', 'event_image', 'event_categories', 'event_tags')
        # read_only_fields = ['user']

class CreateEventSerializer(ModelSerializer):
    event_image = serializers.ImageField(required=False)

    class Meta:
        model = Event
        fields = ('title', 'date', 'description', 'user_id', 'event_image', 'event_categories', 'event_tags')

    def create(self, validated_data):
        event_categories = validated_data.pop('event_categories', [])
        event_tags = validated_data.pop('event_tags', [])
        event_image = validated_data.pop('event_image', None)
        
        if event_image:
            image_instance = Image.objects.create(file=event_image)
            event = Event.objects.create(event_image=image_instance, **validated_data)
        else:
            event = Event.objects.create(**validated_data)
        
        event.event_categories.set(event_categories)
        event.event_tags.set(event_tags)
        return event