from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from courses.models import Course, Sector

# Create your views here.
class CoursesHomeView(APIView):
    def get(self, request, *args, **kwargs):
        sectors=Sector.objects.order_by('?')[:6]
        sector_response=[]
        
        for sector in sectors:
            sector_courses=sector.related_courses.order_by('?')[:4]
            courses_serializer=CourseDisplaySerializer(sector_courses,many=True)
            sector_obj={
                "sector_name": sector.name,
                "sector_uuid": sector.sector_uuid,
                "featured_courses": courses_serializer.data,
                "sector_image":sector.sector_image.url
            }
            sector_response.append(sector_obj)
            
        return Response(data=sector_response,status=status.HTTP_200_OK)
