from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from parmetricapi.models import TeeBox, Course


class TeeBoxSerializer(serializers.ModelSerializer):

    class Meta:
        model = TeeBox
        fields = ("id", "course", "color", "total_yardage")


class TeeBoxes(ViewSet):

    def create(self, request):

        course = Course.objects.get(pk=request.data["course_id"])

        if course.user != request.auth.user:
            return Response(
                {"message": "You can only add tee boxes to courses you have created."},
                status=status.HTTP_403_FORBIDDEN,
            )

        tee_box = TeeBox.objects.create(
            course=course,
            color=request.data["color"],
            total_yardage=request.data["total_yardage"],
        )

        serializer = TeeBoxSerializer(tee_box)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
