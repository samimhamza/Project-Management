# from projects.models import Project
# from projects.api.project.serializers import ProjectSerializer2
# from djangochannelsrestframework.generics import GenericAsyncAPIConsumer
# from djangochannelsrestframework.mixins import (
#     ListModelMixin,
#     RetrieveModelMixin,
#     PatchModelMixin,
#     UpdateModelMixin,
#     CreateModelMixin,
#     DeleteModelMixin,
# )
# from rest_framework import status
# from djangochannelsrestframework.decorators import action
# from djangochannelsrestframework.consumers import GenericAsyncAPIConsumer
# from djangochannelsrestframework.observer import model_observer
# from djangochannelsrestframework.decorators import action


# class ProjectConsumer(GenericAsyncAPIConsumer):
#     queryset = Project.objects.all()
#     serializer_class = ProjectSerializer2

#     @model_observer(Comments)
#     async def comment_activity(
#         self,
#         message: ProjectSerializer2,
#         observer=None,
#         subscribing_request_ids=[]
#         ** kwargs
#     ):
#         await self.send_json(dict(message.data))

#     @comment_activity.serializer
#     def comment_activity(self, instance: Project, action, **kwargs) -> ProjectSerializer2:
#         """This will return the comment serializer"""
#         return ProjectSerializer2(instance)

#     @action()
#     async def subscribe_to_comment_activity(self, request_id, **kwargs):
#         await self.comment_activity.subscribe(request_id=request_id)
