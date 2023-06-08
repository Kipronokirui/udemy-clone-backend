from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.http import HttpResponseBadRequest, HttpResponseNotAllowed
from courses.models import Course, Sector
from .serializers import (CourseDisplaySerializer, CourseUnpaidSerializer, 
                          CoursesListSerializer, CommentSerializer , 
                          CartItemSerializer, CoursePaidSerializer)
from django.db.models import Q
import json
from django.conf import settings
from users.models import User
from decimal import Decimal

# User = settings.AUTH_USER_MODEL
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
                "sector_image":sector.sector_image.url,
                "sector_image":sector.get_image_absolute_url()
            }
            sector_response.append(sector_obj)
            
        return Response(data=sector_response,status=status.HTTP_200_OK)
    
class CourseDetailView(APIView):
    def get(self, request, course_uuid, *args, **kwargs):
        course = Course.objects.filter(course_uuid=course_uuid)
        
        if not course:
            return HttpResponseBadRequest("Course does not exist!")
        
        serializer = CourseUnpaidSerializer(course[0])
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    
class SectorCoursesView(APIView):
    def get(self, request, sector_uuid, *args, **kwargs):
        sector = Sector.objects.filter(sector_uuid=sector_uuid)
        
        if not sector:
            return HttpResponseBadRequest("Sector matching query does not exist!")
        
        sector_courses = sector[0].related_courses.all()
        serializer = CoursesListSerializer(sector_courses, many=True)
        
        total_students=0
        for course in sector_courses:
            total_students+=course.get_enrolled_students()
            
        return Response({
            'data':serializer.data, 
            'sector_name':sector[0].name, 
            'total_students':total_students
            }, status=status.HTTP_200_OK)

class SearchCourseView(APIView):
    def get(self, request, search_term):
        matches=Course.objects.filter(Q(title__icontains=search_term) | Q(description__icontains=search_term))
        serializer = CoursesListSerializer(matches, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK )

class AddComment(APIView):
    permission_classes=[IsAuthenticated]
    def post(self, request, course_uuid):
        try:
            course = Course.objects.get(course_uuid=course_uuid)
        except Course.DoesNotExist:
            return HttpResponseBadRequest('Course does not exist')
        
        content = json.loads(request.body)
        
        # Check if message is in posted data
        if not content.get('message'):
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        serializer = CommentSerializer(data=content)
        
        if serializer.is_valid():
            author = request.user
            # author = User.objects.get(id=1) #We are using id=1 before implementing the user authentication
            comment = serializer.save(user=author)
            course.comment.add(comment) #Add comment to the many to many course comments field
            
            return Response(status=status.HTTP_201_CREATED)
        
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class GetCartDetails(APIView):
    def post(self, request):
        try:
            body=json.loads(request.body)
        except json.decoder.JSONDecodeError:
            return HttpResponseBadRequest()
        
        if type(body.get('cart')) != list:
            return HttpResponseBadRequest()
        
        if len(body.get('cart')) == 0:
            return Response(data=[]) #Returning empty data if there is no data in the cart
        
        courses = []
        for uuid in body.get('cart'):
            item = Course.objects.filter(course_uuid=uuid)
            
            if not item:
                return HttpResponseBadRequest()
            
            courses.append(item[0])
              
        # serializer for cart
        serializer =CartItemSerializer(courses,many=True)
        cart_total=Decimal(0.00)
        for item in serializer.data:
            cart_cost+=Decimal(item.get("price"))
        
        return Response(data={"cart_detail":serializer.data,"cart_total":str(cart_cost)})
    
class CourseStudy(APIView):
    permission_classes=[IsAuthenticated]
    def get(self, request, course_uuid):
        try:
            course = Course.objects.get(course_uuid=course_uuid)
        except Course.DoesNotExist:
            return HttpResponseBadRequest('Course does not exist')
        
        user_courses = request.user.paid_courses.filter(course_uuid=course_uuid)
        if not user_courses:
            return HttpResponseNotAllowed('User is not subscribed to this course')
        serializer = CoursePaidSerializer(course)
        return Response(serializer.data, status=status.HTTP_200_OK)