from api.models import User
from rest_framework import generics
from api.serializers import UserDeleteSerializer
from rest_framework.permissions import IsAuthenticated
from api.tasks import send_delete_notification_email

class UserDeleteAPIView(generics.DestroyAPIView):
    serializer_class = UserDeleteSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user
    
    def perform_destroy(self, instance):
        email = instance.email
        username = instance.username
        instance.delete()
        send_delete_notification_email.delay(username=username, email=email)
        return super().perform_destroy(instance)