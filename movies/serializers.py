from rest_framework import serializers

from .models import Movie, Review

class ReviewCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = "__all__"

class ReviewListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ("name", "text", "parent")

class MovieListSerilizer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ('title', 'tagline', 'category')

class MovieDetailSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(slug_field='name', read_only=True)
    directors = serializers.SlugRelatedField(slug_field='name', read_only=True, many=True)
    actors = serializers.SlugRelatedField(slug_field='name', read_only=True, many=True)
    genre = serializers.SlugRelatedField(slug_field='name', read_only=True, many=True)
    reviews = ReviewListSerializer(many=True)

    class Meta:
        model = Movie
        exclude = ("draft",)