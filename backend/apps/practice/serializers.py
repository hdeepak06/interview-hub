from rest_framework import serializers
from .models import CodingProblem, SQLExercise

class CodingProblemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CodingProblem
        fields = '__all__'

class SQLExerciseSerializer(serializers.ModelSerializer):
    class Meta:
        model = SQLExercise
        fields = '__all__'

