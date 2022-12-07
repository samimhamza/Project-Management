# from django.urls import re_path
from . import consumers

# # websocket_urlpatterns = [
# #     re_path(r'ws/projects/$', consumers.ProjectCunsumers.as_asgi()),
# # ]

# websocket_urlpatterns = [
# ]
from django.urls import re_path
from djangochannelsrestframework.consumers import view_as_consumer
from projects.api.project.views import ProjectViewSet

websocket_urlpatterns = [
    # re_path(r"^user/$", view_as_consumer(ProjectViewSet.as_view())),
    re_path(r"^ws/projects/$", consumers.ProjectCunsumers.as_asgi()),

]
