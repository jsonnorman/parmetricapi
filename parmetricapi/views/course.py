from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from parmetricapi.models import Course


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ("id", "name", "par", "user")


class Courses(ViewSet):
    def list(self, request):
        courses = Course.objects.all()
        serializer = CourseSerializer(courses, many=True)

        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        try:
            course = Course.objects.get(pk=pk)
            serializer = CourseSerializer(course)
            return Response(serializer.data)

        except Course.DoesNotExist:
            return Response(None, status=status.HTTP_404_NOT_FOUND)

    def create(self, request):
        course = Course()
        course.name = request.data["name"]
        course.par = request.data["par"]
        course.user = request.auth.user
        course.save()

        serializer = CourseSerializer(course)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        try:
            course = Course.objects.get(pk=pk)

            if course.user != request.auth.user:
                return Response(
                    {"message": "You do not own this course"},
                    status=status.HTTP_403_FORBIDDEN,
                )

            course.name = request.data["name"]
            course.par = request.data["par"]
            course.save()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Course.DoesNotExist:
            return Response(
                {"message": "Course not found"}, status=status.HTTP_404_NOT_FOUND
            )

    def destroy(self, request, pk=None):
        try:
            course = Course.objects.get(pk=pk)

            if course.user != request.auth.user:
                return Response(
                    {"message": "You do not have permission to delete this course."},
                    status=status.HTTP_403_FORBIDDEN,
                )

            course.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Course.DoesNotExist:
            return Response(None, status=status.HTTP_404_NOT_FOUND)
