from rest_framework import generics, mixins
from projects.models import Project
from projects.api.serializers import ProjectSerializer


class ProjectListCreateAPIView(
    mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView
):
    queryset = Project.objects.filter(deleted_at__isnull=True)
    serializer_class = ProjectSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
