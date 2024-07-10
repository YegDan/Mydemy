from .models import User
from django.http import JsonResponse
from .serializers import UserSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import boto3
from botocore.exceptions import ClientError
from user.settings import COGNITO_CONFIG

cognito_client = boto3.client('cognito-idp', region_name=COGNITO_CONFIG['region'])
#get all users
@api_view(['GET'])
def user_list(request):
    if(request.method == 'GET'):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return JsonResponse({"users":serializer.data}, safe=True)
    
        
#register a user
@api_view(['POST']) 
def register_user(request):
    if request.method == 'POST':
        fname = request.data.get('fname')
        lname = request.data.get('lname')
        email = request.data.get('email')
        password = request.data.get('password')

        try:
            response = cognito_client.sign_up(
                ClientId=COGNITO_CONFIG['app_client_id'],
                Username=email,
                Password=password,
                UserAttributes=[
                    {
                        'Name': 'email',
                        'Value': email
                    },
                    {
                        'Name': 'given_name',
                        'Value': fname
                    },
                    {
                        'Name': 'family_name',
                        'Value': lname
                    }
                ]
            )
            seriliazer = UserSerializer(data=request.data)
            if response['ResponseMetadata']['HTTPStatusCode'] == 200:
                if seriliazer.is_valid():
                    seriliazer.save()
                    return JsonResponse(seriliazer.data, status=201)
            else:
                return JsonResponse({'error' : 'Failed to save user locally'}, status=400)

            
        except ClientError as e:
            error_ms = e.response['Error']['Message']
            return JsonResponse({'error': error_ms}, status=400 )
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
        
     



#still working on this
@api_view(['GET', 'PUT', 'DELETE'])
def user_detail(request, id):
    try:
        user = User.objects.get(id=id)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = UserSerializer(user)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)