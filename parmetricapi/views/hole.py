from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from parmetricapi.models import Hole, TeeBox


class HoleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Hole
        fields = ("id", "tee_box", "hole_number", "yardage", "par", "handicap")


class Holes(ViewSet):

    def list(self, request):

        holes = Hole.objects.all()

        tee_box_id = request.query_params.get("tee_box", None)

        if tee_box_id is not None:
            holes = holes.filter(tee_box_id=tee_box_id)

        serializer = HoleSerializer(holes, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):

        try:
            hole = Hole.objects.get(pk=pk)
            serializer = HoleSerializer(hole)
            return Response(serializer.data)

        except Hole.DoesNotExist:
            return Response(None, status=status.HTTP_404_NOT_FOUND)

    def create(self, request):

        tee_box = TeeBox.objects.get(pk=request.data["tee_box_id"])

        if tee_box.course.user != request.auth.user:
            return Response(
                {"message": "You can only add holes to courses you have created."},
                status=status.HTTP_403_FORBIDDEN,
            )

        hole = Hole.objects.create(
            tee_box=tee_box,
            hole_number=request.data["hole_number"],
            yardage=request.data["yardage"],
            par=request.data["par"],
            handicap=request.data["handicap"],
        )

        serializer = HoleSerializer(hole)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):

        try:
            hole = Hole.objects.get(pk=pk)

            if hole.tee_box.course.user != request.auth.user:
                return Response(
                    {"message": "You can only edit holes for courses you created."},
                    status=status.HTTP_403_FORBIDDEN,
                )

            hole.hole_number = request.data["hole_number"]
            hole.yardage = request.data["yardage"]
            hole.par = request.data["par"]
            hole.handicap = request.data["handicap"]
            hole.save()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Hole.DoesNotExist:
            return Response(
                {"message": "Hole not found"}, status=status.HTTP_404_NOT_FOUND
            )

    def destroy(self, request, pk=None):

        try:
            hole = Hole.objects.get(pk=pk)

            if hole.tee_box.course.user != request.auth.user:
                return Response(
                    {"message": "You can only delete holes for courses you created."},
                    status=status.HTTP_403_FORBIDDEN,
                )

            hole.delete()
            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Hole.DoesNotExist:
            return Response(None, status=status.HTTP_404_NOT_FOUND)
