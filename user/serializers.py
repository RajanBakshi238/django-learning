from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

User = get_user_model()

class UserSignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    confirm_password = serializers.CharField(write_only=True, required=True)

    class Meta: 
        model = User
        fields = [
            'id',
            'name',
            'email',
            'password',
            'confirm_password',
            'date_of_birth',
            'gender'
        ]
        extra_kwargs = {
            'email': {'required': True},
            'name': {'required': True},
            'date_of_birth': {'required': True},
            'gender': {'required': True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError({"password": "Passwords do not match"})
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('confirm_password')
        user = User.objects.create_user(
            name = validated_data['name'],
            email = validated_data['email'],
            date_of_birth = validated_data['date_of_birth'],
            gender = validated_data['gender'],
            password = validated_data['password']
        )

        return user
    
class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if not email or not password:
            raise serializers.ValidationError("Both email and password are required to log in.")    
        
        return attrs