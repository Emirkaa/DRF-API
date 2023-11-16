from rest_framework import serializers,permissions
from .models import *
from drf_extra_fields.fields import Base64ImageField


class ProductSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Product
        img_fields = Base64ImageField()
        fields = '__all__'


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ['quantity','product','user']



class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['name','body','product','user']




class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email','password','id']
        extra_kwargs = {
            'password':{'write_only':True}
        }

    def create(self,validated_data):
        password = validated_data.pop('password',None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance


