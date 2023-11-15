from rest_framework import serializers
from todoapplication.models import Todo
class TodoSerializer(serializers.ModelSerializer):
    user=serializers.CharField(read_only=True)
    class Meta:
        model=Todo
        fields="__all__"

    def create(self, validated_data):
        user=self.context.get('user')
        return Todo.objects.create(**validated_data,user=user)
    