from rest_framework import serializers

from course.models.course import Group


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = (
            'id',
            'name',
            'teacher'
        )


class GroupNameSerializer(serializers.Serializer):
    name = serializers.CharField()
    
