from datetime import datetime, timedelta
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Q
from api.permission.uid import IsAuthenticated
from api.serialiser.profile import FriendRequestSerialiser, ProfileSerializer
from api.validators.email import EmailValidator
from .models import FriendRequests, UserProfile
from django.contrib.auth import authenticate
from .pagination.paginate import PageNumberPagination
from django.utils import timezone


# Create your views here.

class Authentication(APIView):
    def post(self, request):
        request_type = request.data.get('request_type',None)
        email = request.data.get('email',None)
        password = request.data.get('password',None)
        if request_type == 'login':
            user = UserProfile.objects.get(email=email)
            try:
                user = authenticate(username = user.username, password=password)
                if user is not None:
                    response = Response()
                    response.set_cookie('uid', user.pk) #Can use JWT Token or similar for production
                    response.data = {'message':'User authenticated'}
                    response.status_code = 200
                    return response
                else:
                    return Response({'error':'Invalid credentials'}, status=400)
            except UserProfile.DoesNotExist:
                return Response({'error':'User not found'}, status=404)
            except UserProfile.MultipleObjectsReturned:
                return Response({'error':'Multiple users found'}, status=400)
        elif request_type == 'signup':
            date_of_birth = request.data.get('date_of_birth',None)
            location = request.data.get('location',None)
            website = request.data.get('website',None)
            username = email.split('@')[0]
            bio = request.data.get('bio',None)
            user = UserProfile.objects.create_user(
                email=email, 
                password=password, 
                date_of_birth=date_of_birth, 
                location=location, 
                website=website, 
                bio=bio,
                username=username
            )
            return Response({'success':'User created'}, status=200)
        else:
            return Response({'error':'Invalid request type'}, status=400)

    
class Search(APIView):
    permission_classes = [IsAuthenticated]

    def post(self,request):
        search_query = request.data.get('search_query',None)
        if search_query is None:
            return Response({'error':'Search query not found'}, status=400)
        if EmailValidator.validate(search_query):
            users = UserProfile.objects.filter(email=search_query).exclude(
                pk=request.COOKIES.get('uid')
                
            ).exclude(
                is_superuser=True
            )
        else:
            users = UserProfile.objects.filter(
                Q(
                    first_name__icontains=search_query
                ) | Q(
                    last_name__icontains=search_query
                )
            ).exclude(
                pk=request.COOKIES.get('uid')
                
            ).exclude(
                is_superuser=True
            ).distinct()

        paginator = PageNumberPagination()
        page = paginator.paginate_queryset(users, request)
        if page is not None:
            serializer = ProfileSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)
        serializer = ProfileSerializer(users, many=True)
        return paginator.get_paginated_response(serializer.data)

class FriendRequestView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request_type = request.data.get('request_type', None)
        if request_type == 'send':
            receiver = UserProfile.objects.get(pk=request.data.get('receiver', None))
            sender = UserProfile.objects.get(pk=request.COOKIES.get('uid'))
            if FriendRequests.objects.filter(sender=sender, created_at__gte=timezone.now()-timedelta(minutes=1)).count() >= 3:
                return Response({'error': 'Exceeded maximum number of requests'}, status=400)
            if sender == receiver:
                return Response({'error': 'Cannot send request to self'}, status=400)
            if sender.following.filter(pk=receiver.pk).exists():
                return Response({'error': 'Already following'}, status=400)
            if sender._followers.filter(pk=receiver.pk).exists():
                return Response({'error': 'Already followed'}, status=400)
            if FriendRequests.objects.filter(sender=sender, receiver=receiver).exists():
                return Response({'error': 'Request already sent'}, status=400)
            if FriendRequests.objects.filter(sender=receiver, receiver=sender).exists():
                return Response({'error': 'Request already sent'}, status=400)
            
            
                
            friend_request = FriendRequests.objects.create(sender=sender, receiver=receiver)
            return Response({'success': 'Request sent'}, status=200)

        elif request_type == 'accept':
            sender = UserProfile.objects.get(pk=request.data.get('sender', None))
            receiver = UserProfile.objects.get(pk=request.COOKIES.get('uid'))
            
            friend_request = FriendRequests.objects.filter(sender=sender, receiver=receiver).first()
            if friend_request:
                sender.followers.add(receiver)
                receiver.following.add(sender)
                friend_request.delete()
                return Response({'success': 'Request accepted'}, status=200)
            else:
                return Response({'error': 'Request not found'}, status=404)

        elif request_type == 'reject':
            sender = UserProfile.objects.get(pk=request.data.get('sender', None))
            receiver = UserProfile.objects.get(pk=request.COOKIES.get('uid'))
            
            friend_request = FriendRequests.objects.filter(sender=sender, receiver=receiver).first()
            if friend_request:
                friend_request.delete()
                return Response({'success': 'Request rejected'}, status=200)
            else:
                return Response({'error': 'Request not found'}, status=404)

        else:
            return Response({'error': 'Invalid request type'}, status=400)
    
    def get(self,request):
        user = UserProfile.objects.get(pk=request.COOKIES.get('uid'))
        depth=int(request.GET.get('depth',0))

        friend_requests = FriendRequests.objects.filter(receiver=user)
        serializer = FriendRequestSerialiser(friend_requests,depth=depth, many=True)

        page = PageNumberPagination()
        paginator = page.paginate_queryset(friend_requests, request)
        if paginator is not None:
            return page.get_paginated_response(serializer.data)
        

        return page.get_paginated_response(serializer.data)