from rest_framework import serializers
from django.contrib.auth import authenticate
from support.models import User,Department


# class LoginSerializer(serializers.Serializer):
#     email_or_phone = serializers.CharField()
#     password = serializers.CharField()

#     def validate(self, data):
#         user = authenticate(email_or_phone=data.get("email_or_phone"), password=data.get("password"))
#         if user and user.is_active:
#             return user
#         raise serializers.ValidationError("Unable to log in with provided credentials..")

class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        email = data.get("email", None)
        password = data.get("password", None)

        user = authenticate(username=email, password=password)
        if user is None:
            raise serializers.ValidationError(
                'A user with this email and password is not found.'
            )
        # try:
        #     payload = jwt_payload_handler(user)
        #     jwt_token = jwt_encode_handler(payload)
        #     data["token"] = jwt_token
        # except ImportError:
        #     pass

        data["user"] = user
        return data

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'name','password', 'email_or_phone', 'mobile_number', 'department', 'role')
        #START
    #     extra_kwargs = {'password': {'write_only': True}}

    # def create(self, validated_data):
    #     user = User.objects.create(**validated_data)
    #     user.set_password(validated_data['password'])
    #     user.save()
    #     return user

        #END

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'