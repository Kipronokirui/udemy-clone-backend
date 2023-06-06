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

class CommentSerializer(ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model=Comment
        exclude = ['id']
        
class EpisodeUnpaidSerializer(ModelSerializer):
    length = serializers.CharField(source='get_video_length_time')
    class Meta:
        model = Episode
        # fields = ['title', 'file', 'length'] Exclude the file field if the user has not paid for the course
        exclude = ['file']

class CourseSectionUnpaidSerializer(ModelSerializer):
    episodes=EpisodeUnpaidSerializer(many=True)
    total_duration = serializers.CharField(source='total_length')
    class Meta:
        model = CourseSection
        fields = ['section_title', 'episodes', 'total_duration']
           
class CourseUnpaidSerializer(ModelSerializer):
    comment=CommentSerializer(many=True)
    author = UserSerializer()
    course_sections = CourseSectionUnpaidSerializer(many=True)
    student_no = serializers.IntegerField(source='get_enrolled_students')
    total_lectures = serializers.IntegerField(source='get_total_lectures')
    total_duration = serializers.CharField(source='total_course_length')
    image_url = serializers.CharField(source='get_image_absolute_url')
    
    class Meta:
        model = Course
        exclude = ['id']
        
class CoursesListSerializer(ModelSerializer):
    student_no = serializers.IntegerField(source='get_enrolled_students')
    author = UserSerializer()
    description = serializers.CharField(source='get_brief_description')
    total_lectures = serializers.IntegerField(source='get_total_lectures')
    
    class Meta:
        model = Course
        fields = [
            'course_uuid',
            'title',
            'student_no',
            'author',
            'price',
            'image_url',
            'description',
            'total_lectures'
        ]