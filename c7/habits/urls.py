from django.urls import path

from habits.apps import HabitsConfig
from habits.views import HabitListAPIView, HabitRetrieveAPIView, \
    HabitCreateAPIView, HabitUpdateAPIView, \
    HabitDestroyAPIView, PublicHabitListAPIView

app_name = HabitsConfig.name

urlpatterns = [
    path('', HabitListAPIView.as_view(), name='habit_list'),
    path('public/', PublicHabitListAPIView.as_view(),
         name='public_habit_list'),
    path('<int:pk>/', HabitRetrieveAPIView.as_view(),
         name='habit_detail'),
    path('create/', HabitCreateAPIView.as_view(), name='habit_create'),
    path('update/<int:pk>/', HabitUpdateAPIView.as_view(),
         name='habit_update'),
    path('delete/<int:pk>/', HabitDestroyAPIView.as_view(),
         name='habit_delete'),
]
