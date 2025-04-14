from rest_framework import serializers
from .models import APIModel

class APIModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = APIModel
        fields = '__all__'


from .models import CodePuzzle
from rest_framework import serializers

class CodePuzzleSerializer(serializers.ModelSerializer):
    class Meta:
        model = CodePuzzle
        fields = '__all__'


from .models import Submission

class SubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submission
        fields = ['puzzle', 'code_submitted']
