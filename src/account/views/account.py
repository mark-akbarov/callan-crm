from rest_framework.viewsets import ModelViewSet

from account.models.account import User, Enrollment
from account.serializers.account import UserSerializer, EnrollmentSerializer


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    

class EnrollmentViewSet(ModelViewSet):
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer
    
