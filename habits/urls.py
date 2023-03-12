from habits.views import HabitCreateListView, HabitRetrieveUpdateDestroyAPIView, ForeignHabitsListView
from django.urls import path


urlpatterns = [
    path('', HabitCreateListView.as_view(), name='create_and_list_habits'),
    path('foreign/', ForeignHabitsListView.as_view(), name='foreign_habits'),
    path('<int:pk>/', HabitRetrieveUpdateDestroyAPIView.as_view(), name='retrieve_update_delete_habit')
]

