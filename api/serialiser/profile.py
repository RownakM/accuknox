from rest_framework.serializers import ModelSerializer,SerializerMethodField
from api.models import UserProfile,FriendRequests

class ProfileSerializer(ModelSerializer):
    friend_requests = SerializerMethodField()
    class Meta:
        model=UserProfile
        exclude=['password',"is_superuser","is_staff","is_active","date_joined"]

    def get_friend_requests(self,obj):
        return obj.count_friend_requests()


class FriendRequestSerialiser(ModelSerializer):
    def __init__(self, *args, **kwargs):
        depth = kwargs.pop('depth', None)  # Extract depth parameter from kwargs
        super().__init__(*args, **kwargs)
        if depth is not None:
            self.Meta.depth = depth
    class Meta:
        model=FriendRequests
        exclude=["created_at"]