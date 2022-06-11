from projects.api.serializers import AttachmentSerializer
from projects.models import Attachment
from rest_framework import viewsets, status
from common.actions import delete


class AttachmentViewSet(viewsets.ModelViewSet):
    queryset = Attachment.objects.all()
    serializer_class = AttachmentSerializer

    def destroy(self, request, pk=None):
        return delete(self, request, Attachment, 'attachment')
