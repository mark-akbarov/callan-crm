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