
from users import models
from rest_framework import serializers


class UserRegisterSerializer(serializers.ModelSerializer):
    """Serializes a user object"""

    class Meta:
        model = models.User
        fields = ('id', 'email', 'name', 'password', 'school', 'class_number', 'city', 'mobile')
        extra_kwargs = {
            'password': {
                'write_only': True,
                'style': {
                    'input_type': 'password'
                }
            }
        }
    
    def create(self, validated_data):
        """Create and return a new user"""
        user = models.User.objects.create_user(
            email=validated_data['email'],
            name=validated_data['name'],
            password=validated_data['password'],
            school=validated_data['school'],
            class_number=validated_data['class_number'],
            city=validated_data['city'],
            mobile=validated_data['mobile']
        )
        return user