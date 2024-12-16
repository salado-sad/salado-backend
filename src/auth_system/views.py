from django.contrib.auth import authenticate, login
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated

from .serializers import SaladoUserSerializer
from .models import SaladoUser

class SignUpView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):

        # TODO: make front ok
        mapped_data = {
            'first_name': request.data.get('name'),
            'last_name': request.data.get('lastname'),
            'email': request.data.get('email'),
            'date_of_birth': request.data.get('birthdate'),
            'phone_number': request.data.get('phone'),
            'national_code': request.data.get('nationalcode'),
            'password': request.data.get('password'),
        }

        serializer = SaladoUserSerializer(data=mapped_data)
        if serializer.is_valid():
            phone_number = serializer.validated_data['phone_number']
            national_code = serializer.validated_data['national_code']
            email = serializer.validated_data['email']
            if not validate_phone_number(phone_number):
                return Response({'error': 'Phone number must be exactly 10 digits.'}, status=status.HTTP_400_BAD_REQUEST)

            if not validate_national_code(national_code):
                return Response({'error': 'National code must be exactly 10 digits.'}, status=status.HTTP_400_BAD_REQUEST)

            if '@' not in email or '.' not in email.split('@')[-1]:
                return Response({'error': 'Invalid email format.'}, status=status.HTTP_400_BAD_REQUEST)

            if not validate_phone_number_with_national_code(phone_number, national_code):
                return Response({'error': 'Phone number does not match with national code.'}, status=status.HTTP_400_BAD_REQUEST)

            user = serializer.save()
            user.is_active = False
            # Send verification email
            self.send_verification_email(user)
            user.save()
            return Response({'message': 'User created successfully. Verification email sent.'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def send_verification_email(user):
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        # TODO: make it better
        verification_link = f'http://localhost:8000/auth/verify/{uid}/{token}/'

        send_mail(
            subject='Verify your email',
            message=f'Click the link to verify your email: {verification_link}',
            from_email='auth@salado.mghgm.ir',
            recipient_list=[user.email],
            fail_silently=False,
        )

def validate_national_code(national_code):
    if not national_code.isdigit() or len(national_code) != 10:
        return False

    check_digit = int(national_code[-1])

    weighted_sum = sum(int(national_code[i]) * (10 - i) for i in range(9))

    remainder = weighted_sum % 11

    if remainder < 2:
        return check_digit == remainder
    else:
        return check_digit == (11 - remainder)


def validate_phone_number(phone_number):
    if phone_number.startswith("09") and len(phone_number) == 11 and phone_number.isdigit():
        return True
    return False

def validate_phone_number_with_national_code(phone_number, nationalcode):
    return True

class VerifyEmailView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = SaladoUser.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, SaladoUser.DoesNotExist):
            return Response({'error': 'Invalid token or user ID'}, status=status.HTTP_400_BAD_REQUEST)

        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return Response({'message': 'Email verification successful'}, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid or expired token'}, status=status.HTTP_400_BAD_REQUEST)

class SignInView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            return Response(
                {'error': 'Both username/email and password are required.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = SaladoUser.objects.filter(username=email).first()
        if user:
            # user = authenticate(username=user.username, password=user.password)
            # WHy not working??
            if user.check_password(password):
                if not user.is_active:
                    return Response(
                        {'error': 'Your account is inactive. Please verify your email.'},
                        status=status.HTTP_403_FORBIDDEN
                    )

                login(request, user)
                return Response({'message': 'Login successful.'}, status=status.HTTP_200_OK)
            else:
                return Response(
                    {'error': 'Invalid credentials. Please try again.'},
                    status=status.HTTP_401_UNAUTHORIZED
                )

        return Response(
            {'error': 'User not found. Please check your username/email.'},
            status=status.HTTP_404_NOT_FOUND
        )

class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if not request.user.is_active:
            return Response({'error': 'User not verified.'}, status=status.HTTP_403_FORBIDDEN)
        serializer = SaladoUserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)
