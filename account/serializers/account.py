from rest_framework import serializers

from account.models.account import User, Enrollment


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'first_name',
            'last_name',
            'type',
            'phone_number',
            'email',
            'telegram_username',
            'telegram_user_id',
            ]


class EnrollmentSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Enrollment
        fields = [
            'id',
            'user',
            'course',
            'knowledge_level'
        ]
        
    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user_instance = UserSerializer.create(UserSerializer(), validated_data=user_data)

        enrollment_instance = Enrollment.objects.create(user=user_instance, **validated_data)
        return enrollment_instance
