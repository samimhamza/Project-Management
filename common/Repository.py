from common.actions import delete, withTrashed, trashList, restore
from common.custom import CustomPageNumberPagination
from rest_framework.decorators import action
from rest_framework import viewsets


class Repository(viewsets.ModelViewSet):
    model = None
    order_by = "-created_at"
    pagination_class = CustomPageNumberPagination
    serializer_action_classes = {}
    queryset_actions = {}

    def destroy(self, request, pk=None):
        return delete(self, request, self.model)

    @action(detail=False, methods=["get"])
    def all(self, request):
        return withTrashed(self, self.model, order_by=self.order_by, request=request)

    @action(detail=False, methods=["get"])
    def trashed(self, request):
        return trashList(self, self.model)

    @action(detail=False, methods=["put"])
    def restore(self, request, pk=None):
        return restore(self, request, self.model)

    def get_serializer_class(self):
        try:
            return self.serializer_action_classes[self.action]
        except(KeyError, AttributeError):
            return super().get_serializer_class()

    def get_queryset(self):
        try:
            return self.queryset_actions[self.action]
        except (KeyError, AttributeError):
            return super().get_queryset()
