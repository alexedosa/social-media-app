from rest_framework import serializers
from .models import Profile

class ProfileSerializer(serializers.ModelSerializer):
    # To see the username instead of just the user ID; source = ;
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Profile
        fields = '__all__' 
