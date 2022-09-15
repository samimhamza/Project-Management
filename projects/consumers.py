from projects.models import Project
from projects.api.project.serializers import ProjectSerializer2
from djangochannelsrestframework.generics import GenericAsyncAPIConsumer
from djangochannelsrestframework.mixins import (
    ListModelMixin,
    RetrieveModelMixin,
    PatchModelMixin,
    UpdateModelMixin,
    CreateModelMixin,
    DeleteModelMixin,
)
from rest_framework import status
from djangochannelsrestframework.decorators import action
from djangochannelsrestframework.consumers import GenericAsyncAPIConsumer
from djangochannelsrestframework.observer import model_observer
from djangochannelsrestframework.decorators import action


class ProjectConsumer(ListModelMixin,
                      RetrieveModelMixin,
                      PatchModelMixin,
                      UpdateModelMixin,
                      CreateModelMixin,
                      DeleteModelMixin, GenericAsyncAPIConsumer):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer2
