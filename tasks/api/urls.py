from tasks.api.views import TaskViewSet, ProjectCommentViewSet, TaskCommentViewSet
from tasks.api.my_project_tasks.views import MyTaskViewSet, MyProjectCommentViewSet, MyTaskCommentViewSet
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r"tasks", TaskViewSet, basename="tasks")
router.register(r"my_tasks", MyTaskViewSet, basename="my_tasks")
router.register(r"project_comments",
                ProjectCommentViewSet, basename="project_comments")
router.register(r"task_comments", TaskCommentViewSet, basename="task_comments")
router.register(r"my_task_comments", MyTaskCommentViewSet,
                basename="my_task_comments")
router.register(r"my_project_comments",
                MyProjectCommentViewSet, basename="my_project_comments")
urlpatterns = router.urls
