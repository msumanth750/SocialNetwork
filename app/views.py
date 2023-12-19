from .models import UserProfile, UserRequest
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer, UserDetailSerializer ,UserProfileSerializer
import json


@api_view(['POST'])
def signup(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            email = data['email'].lower()  # Case insensitive email
            password = data['password']
            first_name = data['first_name']
            last_name = data['last_name']         


            # Check if user with the given email already exists
            if User.objects.filter(email=email).exists():
                return Response({'error': 'User with this email already exists'}, status=status.HTTP_400_BAD_REQUEST)

            user_data = {'email': email, 'password': password,'username':email}
            serializer = UserSerializer(data=user_data)

            if serializer.is_valid():
                user = User.objects.create_user(email=email, password=password,username=email,first_name=first_name,last_name=last_name)
                UserProfile.objects.create(user=user)
                # serializer.save()
                return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except KeyError:
            return Response({'error': 'Invalid request data'}, status=status.HTTP_400_BAD_REQUEST)

    return Response({'error': 'Invalid request method'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['POST'])
def login_user(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            email = data['email'].lower()  # Case insensitive email
            password = data['password']
            print(email,password)

            user = authenticate(request, username=email, password=password)
            print(user)

            if user is not None:
                login(request, user)
                return Response({'message': 'Login successful'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

        except KeyError:
            return Response({'error': 'Invalid request data'}, status=status.HTTP_400_BAD_REQUEST)

    return Response({'error': 'Invalid request method'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def authenticated_api(request):
    # Your authenticated API logic goes here
    return Response({'message': 'Authenticated API response'}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def search_users(request, keyword):
    users_by_email = User.objects.filter(email__icontains=keyword)
    users_by_name = User.objects.filter(username__icontains=keyword)

    results = UserProfile.objects.filter(
        user__in=users_by_email | users_by_name)[:10]
    serializer = UserProfileSerializer(results, many=True)

    return Response(serializer.data, status=status.HTTP_200_OK)


@csrf_exempt
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def send_friend_request(request, friend_id):
    if request.method == 'POST':
        try:
            friend = User.objects.get(id=friend_id)
            user_profile = UserProfile.objects.get(user=request.user)

            current_time = timezone.now()
            user_requests = UserRequest.objects.filter(user=request.user)
            current_minute_requests = user_requests.filter(
                timestamp__minute=current_time.minute).count()

            # Check if user can send more friend requests in minute
            if current_minute_requests >= 3:
                return Response({'error': 'Cannot send more than 3 friend requests within a minute'}, status=status.HTTP_400_BAD_REQUEST)

            # Check if a friend request has already been sent
            if friend in user_profile.friend_requests_sent.all():
                return Response({'error': 'Friend request already sent to this user'}, status=status.HTTP_400_BAD_REQUEST)

            user_profile.friend_requests_sent.add(friend)
            UserRequest.objects.create(user=request.user,friend=friend)
            user_profile.save()

            return Response({'message': 'Friend request sent successfully'}, status=status.HTTP_201_CREATED)

        except User.DoesNotExist:
            return Response({'error': 'Friend not found'}, status=status.HTTP_404_NOT_FOUND)

    return Response({'error': 'Invalid request method'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def accept_friend_request(request, friend_id):
    if request.method == 'POST':
        try:
            friend = User.objects.get(id=friend_id)
            user_profile = UserProfile.objects.get(user=request.user)

            # Check if there's a pending friend request from the user
            if friend not in user_profile.friend_requests_received.all():
                return Response({'error': 'No pending friend request from this user'}, status=status.HTTP_400_BAD_REQUEST)

            # Accept friend request
            user_profile.friends.add(friend)
            user_profile.friend_requests_received.remove(friend)
            user_profile.save()

            return Response({'message': 'Friend request accepted successfully'}, status=status.HTTP_200_OK)

        except User.DoesNotExist:
            return Response({'error': 'Friend not found'}, status=status.HTTP_404_NOT_FOUND)

    return Response({'error': 'Invalid request method'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_friends(request):
    user_profile = UserProfile.objects.get(user=request.user)
    friends = user_profile.friends.all()
    serializer = UserDetailSerializer(friends, many=True)

    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_pending_friend_requests(request):
    user_profile = UserProfile.objects.get(user=request.user)
    pending_requests = user_profile.friend_requests_received.all()
    serializer = UserDetailSerializer(pending_requests, many=True)

    return Response(serializer.data, status=status.HTTP_200_OK)
