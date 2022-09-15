# routing.py
# from django.urls import re_path
# from djangochannelsrestframework.consumers import view_as_consumer
# from projects.api.project.views import ProjectViewSet

# websocket_urlpatterns = [
#     re_path(r"^projects/$",
#             view_as_consumer(ProjectViewSet.as_view({'get': 'list'})))
# ]

# routing.py
from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r"^ws/$", consumers.ProjectConsumer.as_asgi()),
]
