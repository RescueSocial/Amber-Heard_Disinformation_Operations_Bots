from rest_framework import serializers
from .models import Nlutext

class NlutextSerializer(serializers.ModelSerializer):
    trained_at = serializers.DateTimeField(required=False)
    trained = serializers.BooleanField(required=False)
    defense_AH = serializers.FloatField(required=False)
    support_AH = serializers.FloatField(required=False)
    offense_AH = serializers.FloatField(required=False)
    defense_against_AH = serializers.FloatField(required=False)
    class Meta:
        model = Nlutext
        fields = ('id', 'text', 'defense_AH', 'support_AH', 'offense_AH', 
                    'defense_against_AH', 'trained', 'created_at', 'trained_at')

