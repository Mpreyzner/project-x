from rest_framework import serializers
from .models import AuthorStats
from .models import TotalStats


class AuthorStatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuthorStats
        fields = ('author', 'top_10_words')


class TotalStatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TotalStats
        fields = ('top_10_words',)
