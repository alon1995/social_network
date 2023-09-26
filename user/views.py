from rest_framework.response import Response  #  ריספונס לוקחת נתוהים של פייתון או נתונים שעברו סיראלזיציה ותמיר את זנתונים לג'סון
from rest_framework.decorators import api_view
from rest_framework import status
from user.models import *
from .serializers import *
from django.utils import timezone

# Create your views here.



@api_view(['GET'])  # a list of allowed methods
def get_all_users(request):
    all_users = CustomUser.objects.all()
    serializer = CustomUserSerializer(all_users, many=True)  # setting amny to true tells our serializer that we are going to serialize multpule items
    return Response(serializer.data)

@api_view(['POST'])
def create_new_user(requset):
    serializer = CustomUserSerializer(data=requset.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)

@api_view(['DELETE'])
def delete_user(request, pk):
    try:
        user = CustomUser.objects.get(pk=pk)
    except CustomUser.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    # Check if the user making the request is a manager
    if not request.user.is_authenticated or not request.user.is_staff:
        return Response(status=status.HTTP_403_FORBIDDEN)
    
    user.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['PUT', 'PATCH'])  # Allow both PUT and PATCH methods
def updateItem(request, pk):
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




