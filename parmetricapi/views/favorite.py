from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from parmetricapi.models import Favorite, Course


class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = ("id", "user", "course")


class Favorites(ViewSet):

    def list(self, request):

        favorites = Favorite.objects.filter(user=request.auth.user)
        serializer = FavoriteSerializer(favorites, many=True)
        return Response(serializer.data)

    def create(self, request):

        course = Course.objects.get(pk=request.data["course_id"])

        already_favorited = Favorite.objects.filter(
            user=request.auth.user,
            course=course
        ).exists()

        if already_favorited:
            return Response(
                {"message": "Course is already in your favorites."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        favorite = Favorite.objects.create(
            user=request.auth.user,
            course=course
        )

        serializer = FavoriteSerializer(favorite)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, pk=None):

        try:
            favorite = Favorite.objects.get(pk=pk, user=request.auth.user)
            favorite.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Favorite.DoesNotExist:
            return Response(
                {"message": "Favorite not found"},
                status=status.HTTP_404_NOT_FOUND,
            )