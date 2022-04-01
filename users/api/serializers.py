from django.db.models import fields
from rest_framework import serializers
from users.models import User

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'

    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user
    
class updateUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username','email','name','last_name','phone','password')

class PasswordSerializer(serializers.Serializer):
    password = serializers.CharField(max_length = 128,min_length= 6,write_only = True)
    password2 = serializers.CharField(max_length = 128,min_length= 6,write_only = True)

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError({'password': 'Debe ingresar ambas contraseñas iguales'}
            )
        return data

class UserListSerializer(serializers.ModelSerializer):    
    
    class Meta:
        model: User

    def to_representation(self, instance):
        return {
            'id': instance['id'],
            'username': instance['username'],
            'email': instance['email'],
            'name': instance['name'],
            'last_name':instance['last_name'],
            'phone':instance['phone'],
            'password':instance['password'],
}