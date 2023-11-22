from rest_framework.response import Response  #  ריספונס לוקחת נתוהים של פייתון או נתונים שעברו סיראלזיציה ותמיר את זנתונים לג'סון
from rest_framework.decorators import api_view
from rest_framework import status
from user.models import *
from .serializers import *
from django.utils import timezone
from django.contrib.auth.hashers import make_password
from rest_framework.views import APIView
from django.contrib.auth import authenticate, login, logout
from rest_framework.authtoken.models import Token


# Create your views here.

@api_view(['GET'])  # a list of allowed methods
def get_all_users(request):
    all_users = CustomUser.objects.all()
    serializer = CustomUserSerializer(all_users, many=True)  # setting amny to true tells our serializer that we are going to serialize multpule items
    return Response(serializer.data)


@api_view(['POST'])
def signup(request):
    serializer = CustomUserSerializer(data=request.data)
    if serializer.is_valid():
        # Securely hash the user's password before saving
        password = make_password(request.data.get('password'))
        serializer.save(password=password)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def delete_user(request, pk):
    try:
        user = CustomUser.objects.get(pk=pk)
    except CustomUser.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    # Debugging statements
    print(f'User is authenticated: {request.user.is_authenticated}')
    print(f'User is staff: {request.user.is_staff}')

    # Check if the user making the request is a manager
    if not request.user.is_authenticated or not request.user.is_staff:
        return Response(status=status.HTTP_403_FORBIDDEN)
    
    user.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['PUT', 'PATCH'])  # Allow both PUT and PATCH methods
def update_user(request, pk):
    try:
        user = CustomUser.objects.get(pk=pk)
    except CustomUser.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        # For PUT, update all fields with the new data
        serializer = CustomUserSerializer(user, data=request.data)
    elif request.method == 'PATCH':
        # For PATCH, update only the fields provided in the request
        serializer = CustomUserSerializer(user, data=request.data, partial=True)

    if serializer.is_valid():
        # Update the created field with the current date and time
        serializer.validated_data['created'] = timezone.now()

        serializer.save()
        return Response(serializer.data)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CustomUserLoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            user.status = True
            user.save()  # Save the user instance to persist the status change

            login(request, user)
            # Check if an existing token exists for the user
            existing_token = Token.objects.filter(user=user)

            if existing_token:
                # Delete the existing token
                existing_token.delete()

            # Create a new token for the user
            token = Token.objects.create(user=user)
            token.save()

            # Return the token along with the user data
            serializer = CustomUserSerializer(user)
            return Response({
                "token": token.key,
                "user": serializer.data
            })
        else:
            return Response(
                {'error': 'Invalid credentials'},
                status=status.HTTP_401_UNAUTHORIZED
            )

class CustomLogoutView(APIView):
    def post(self, request):
        # Get the user who is currently logged in
        user = request.user

        if user.is_authenticated:
            # Update the status to False when the user logs out
            user.status = False
            user.save()

            # Call the logout method to log the user out
            logout(request)
            return Response({'message': 'Logged out successfully'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'User not logged in'}, status=status.HTTP_400_BAD_REQUEST)
