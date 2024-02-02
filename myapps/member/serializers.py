from rest_framework import serializers

class GetEmail(serializers.Serializer):
    email = serializers.EmailField()

