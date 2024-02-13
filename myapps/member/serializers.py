from rest_framework import serializers

class GetEmail(serializers.Serializer):
    email = serializers.EmailField()

class Code(serializers.Serializer):
    code = serializers.CharField()
    email = serializers.EmailField()

class Active(serializers.Serializer):
    code:serializers.CharField()

