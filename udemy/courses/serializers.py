from rest_framework import serializers
from courses.models import Comment, Course, CourseSection, Episode, Sector
from rest_framework.serializers import ModelSerializer
from users.serializers import UserSerializer

class CourseDisplaySerializer(ModelSerializer):
    # rating=serializers.IntegerField(source='get_rating')
    student_no=serializers.IntegerField(source='get_enrolled_students')
    author=UserSerializer()
    image_url = serializers.CharField(source='get_image_absolute_url')
    class Meta:
        model=Course
        fields=['course_uuid',"title",'student_no',"author","price","image_url"]