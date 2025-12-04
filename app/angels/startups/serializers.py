from django import serializers
from .models import StartupForm, StartupTeamMember, AuthUsers

class StartupFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = StartupForm
        fields = '__all__'


class StartupTeamMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = StartupTeamMember
        fields = '__all__'
        

class LoginSerializer(serializers.ModelSerializer):
    member_email = serializers.CharField(source='member_email', read_only=True)
    member_password = serializers.CharField(source='member_password', read_only=True)

    
        

