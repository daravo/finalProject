from rest_framework import serializers

from .models import Worker, Project

class WorkerSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Worker
        fields = ('__all__')

class ProjectSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Project
        fields = ('__all__')
