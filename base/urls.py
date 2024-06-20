from django.urls import path, include
from .views import TaskList, TaskDetail, TaskCreate, TaskUpdate, TaskDelete

urlpatterns = [
    path('users/', include('users.urls')),
    path('', TaskList.as_view(), name='taskList'),
    path('task/<int:pk>/', TaskDetail.as_view(), name='task'),
    path('task-create/', TaskCreate.as_view(), name='createTask'),
    path('task-update/<int:pk>/', TaskUpdate.as_view(), name='updateTask'),
    path('task-delete/<int:pk>/', TaskDelete.as_view(), name='deleteTask')
]
