from rest_framework import generics, mixins, status
from rest_framework.views import APIView
from projects.models import Project
from projects.api.serializers import ProjectSerializer
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404

# class ProjectListCreateAPIView(
#     mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView
# ):
#     queryset = Project.objects.filter(deleted_at__isnull=True)
#     serializer_class = ProjectSerializer

#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)

#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)


class ProjectListCreateAPIView(APIView):
    def get(self, request):
        projects = Project.objects.filter(deleted_at__isnull=True)
        serializers = ProjectSerializer(projects, many=True)
        return Response(serializers.data)

    def post(self, request):
        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProjectDetailAPIView(APIView):
    def get_object(self, pk):
        project = get_object_or_404(Project, pk=pk)
        return project

    def get(self, request, pk):
        project = self.get_object(pk)
        serializer = ProjectSerializer(project)
        return Response(serializer.data)

    def put(self, request, pk):
        project = self.get_object(pk)
        serializer = ProjectSerializer(project, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
      project = self.get_object(pk)
      project.delete()
      return Response(status=status.HTTP_204_NO_CONTENT)