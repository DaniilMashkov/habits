from habits.services import create_task
from rest_framework import generics, mixins
from habits.serializers import HabitSerializer, Habits


class ForeignHabitsListView(generics.ListAPIView):
    serializer_class = HabitSerializer

    def get_queryset(self):
        return Habits.objects.filter(is_private=False).exclude(user=self.request.user)


class HabitCreateListView(mixins.CreateModelMixin, generics.ListAPIView):
    serializer_class = HabitSerializer

    def get_queryset(self):
        if self.request.user.is_staff:
            return Habits.objects.all()
        return Habits.objects.filter(user=self.request.user)

    def post(self, *args, **kwargs):
        return super().create(*args, **kwargs)

    def perform_create(self, serializer):
        create_task(serializer)


class HabitRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = HabitSerializer

    def get_queryset(self):
        if self.request.user.is_staff:
            return Habits.objects.all()
        return Habits.objects.filter(user=self.request.user)

    def perform_update(self, serializer):
        create_task(serializer)
