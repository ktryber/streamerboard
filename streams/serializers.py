from rest_framework import serializers

from . import models

class StreamPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.StreamPost
        fields = (
            'id',
            'title',
            'description',
            'upvotes',
            'downvotes',
            'created'

        )
