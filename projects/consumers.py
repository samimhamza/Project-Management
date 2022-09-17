from projects.api.project.serializers import ProjectSerializer, ProjectSerializer2
from djangochannelsrestframework.decorators import action
from djangochannelsrestframework.generics import GenericAsyncAPIConsumer
from projects.models import Project
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async


# class ProjectCunsumers(AsyncWebsocketConsumer):
#     async def connect(self):
#         await self.accept()
#         # await self.send({
#         #     "type": "websocket.accept",
#         # })

#     async def receive(self, text_data):
#         text_data_json = json.loads(text_data)
#         data = text_data_json['data']
#         print('ssss', data)
#         await self.send({
#             "type": "project_data",
#             "data": json.dumps(data),
#         })

#      # Receive message from room group
#     async def project_data(self, event):
#         data = event['data']

#         # Send message to WebSocket
#         await self.send(text_data=json.dumps({
#             'data': data
#         }))
#     # async def connect(self):
#     #     # self.room_name = self.scope['url_route']['kwargs']['room_name']
#     #     # self.room_group_name = 'chat_%s' % self.room_name
#     #     # # Join room group
#     #     # await self.channel_layer.group_add(
#     #     #     self.room_group_name,
#     #     #     self.channel_name
#     #     # )
#     #     await self.accept()

#     # # async def disconnect(self, close_code):
#     # #     # Leave room group
#     # #     await self.channel_layer.group_discard(
#     # #         self.room_group_name,
#     # #         self.channel_name
#     # #     )

#     # # Receive message from WebSocket
#     # async def receive(self, text_data):
#     #     text_data_json = json.loads(text_data)
#     #     message = text_data_json['message']

#     #     # Send message to room group
#     #     await self.channel_layer.group_send(
#     #         self.room_group_name,
#     #         {
#     #             'type': 'chat_message',
#     #             'message': message
#     #         }
#     #     )

#     # # Receive message from room group
#     # async def chat_message(self, event):
#     #     message = event['message']

#     #     # Send message to WebSocket
#     #     await self.send(text_data=json.dumps({
#     #         'message': message
#     #     }))


# consumers.py
from djangochannelsrestframework.observer import model_observer


class ProjectCunsumers(GenericAsyncAPIConsumer):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    @action()
    async def broadcastProject(self, pk=None, to=None, **kwargs):
        project = await database_sync_to_async(self.get_object)(pk=pk)
        serializer = await database_sync_to_async(ProjectSerializer(project))
        return serializer.data, 200

    # @model_observer(Project)
    # async def comment_activity(
    #     self,
    #     message: ProjectSerializer,
    #     observer=None,
    #     subscribing_request_ids=[]
    #     ** kwargs
    # ):
    #     await self.send_json(dict(message.data))

    # @comment_activity.serializer
    # def comment_activity(self, instance: Project, action, **kwargs) -> ProjectSerializer:
    #     return ProjectSerializer(instance)

    # @action()
    # async def subscribe_to_comment_activity(self, request_id, **kwargs):
    #     await self.comment_activity.subscribe(request_id=request_id)
