from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.exceptions import ValidationError
from .models import SaladoUser
from .serializers import RegisterSerializer, UserSerializer, CustomTokenObtainPairSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

import re

class RegisterView(CreateAPIView):
    queryset = SaladoUser.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        data = request.data

        if not data.get('phone_number', None) or not self.__validate_phone_number(data['phone_number']):
            print(data)
            return Response({'error': 'Invalid phone number format.'}, status=status.HTTP_400_BAD_REQUEST)

        if not data.get('national_code', None) or not self.__validate_national_code(data['national_code']):
            return Response({'error': 'Invalid national code format.'}, status=status.HTTP_400_BAD_REQUEST)

        if not data.get('email', None) or not self.__validate_email(data['email']):
            return Response({'error': 'Invalid email format.'}, status=status.HTTP_400_BAD_REQUEST)

        if not self.__validate_phone_number_with_national_code(data['phone_number'], data['national_code']):
            return Response({'error': 'National code does not match with phone number.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            response = super().create(request, *args, **kwargs)
            
            # TODO Verification email

            return Response({'message': f'ok!'}, status=status.HTTP_201_CREATED)
        except ValidationError as ve:
            print(type(ve))
            return Response({'error': f'A user with this {list(ve.detail.keys())[0]} information already exists'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': f'User registration failed: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)



    @staticmethod
    def __validate_national_code(national_code):
        if not national_code.isdigit() or len(national_code) != 10:
            return False
    
        check_digit = int(national_code[-1])
    
        weighted_sum = sum(int(national_code[i]) * (10 - i) for i in range(9))
    
        remainder = weighted_sum % 11
    
        if remainder < 2:
            return check_digit == remainder
        else:
            return check_digit == (11 - remainder)
    
    @staticmethod 
    def __validate_phone_number(phone_number):
        if phone_number.startswith("09") and len(phone_number) == 11 and phone_number.isdigit():
            return True
        return False

    @staticmethod 
    def __validate_phone_number_with_national_code(phone_number, nationalcode): 
        return True

    @staticmethod
    def __validate_email(email):
        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        
        if re.match(email_regex, email):
            return True
        else:
            return False


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_profile(request):
    serializer = UserSerializer(request.user)
    return Response(serializer.data)
