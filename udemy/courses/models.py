from django.db import models
import uuid
from decimal import Decimal
from django.conf import settings
from django.contrib.auth import get_user_model
from .helpers import get_timer
from mutagen.mp4 import MP4,MP4StreamInfoError

User = settings.AUTH_USER_MODEL
# Create your models here.
class Sector(models.Model):
    name=models.CharField(max_length=225)
    sector_uuid=models.UUIDField(default=uuid.uuid4,unique=True)
    related_courses=models.ManyToManyField('Course',blank=True)
    # sector_image=models.ImageField(upload_to='sector_images',storage=MediaCloudinaryStorage())
    sector_image=models.ImageField(upload_to='sector_images', blank=True, null=True)
    
    def get_image_absolute_url(self):
        return "http://localhost:8000"+self.sector_image

class Course(models.Model):
    title=models.CharField(max_length=225)
    description=models.TextField()
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)
    # rating=models.ManyToManyField('Rate',blank=True)
    # sector=models.ForeignKey('Sector',on_delete=models.CASCADE)
    # author=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    author=models.ForeignKey(User,on_delete=models.CASCADE)
    student_rating=models.IntegerField(default=0)
    language=models.CharField(max_length=225)
    course_length=models.CharField(default=0,max_length=20)
    course_sections=models.ManyToManyField('CourseSection',blank=True)
    comment=models.ManyToManyField('Comment',blank=True)
    course_uuid=models.UUIDField(default=uuid.uuid4,unique=True)
    # image_url=models.ImageField(upload_to='course_images',storage=MediaCloudinaryStorage())
    price=models.DecimalField(max_digits=5 ,decimal_places=2)
    
    def get_brief_description(self):
        return self.description[:100]
    
    def get_enrolled_students(self):
        students = get_user_model().objects.filter(paid_course=self)
        return len(students)
    def get_total_lectures(self):
        lectures=0
        for section in self.course_sections.all():
            lectures+=len(section.episodes.all())
        return lectures
    def total_course_length(self):
        length=Decimal(0.00)

        for section in self.course_sections.all():
            for episode in section.episodes.all():
                length+=episode.length
       
        return get_timer(length,type="short")
            
    
class CourseSection(models.Model):
    section_title=models.CharField(max_length=225,blank=True,null=True)
    section_number=models.IntegerField(blank=True,null=True)
    episodes=models.ManyToManyField('Episode',blank=True)

    def total_length(self):
        total=Decimal(0.00)
        for episode in self.episodes.all():
            total+=episode.length
        return get_timer(total,type='min')

class Episode(models.Model):
    title=models.CharField(max_length=225)
    # file=CloudinaryField(resource_type='video',validators=[validate_video],folder='media')
    # file=models.FileField(upload_to='courses',validators=[validate_video],)
    file=models.FileField(upload_to='courses', blank=True, null=True)
    length=models.DecimalField(max_digits=100,decimal_places=2)
    
    def get_video_length(self):
        try:
            video=MP4(self.file)
            return video.info.length
            
        except MP4StreamInfoError:
            return 0.0

    def get_video_length_time(self):
        return get_timer(self.length)
    
    def get_absolute_url(self):
        # return self.file.url
        return "http://localhost:8000"+self.file
    
    def save(self,*args, **kwargs):
        self.length=self.get_video_length()
        # print(self.length)
        # print(self.file.path)
        return super().save(*args, **kwargs)

class Comment(models.Model):
    # user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    message=models.TextField()
    created=models.DateTimeField(auto_now=True)
    
