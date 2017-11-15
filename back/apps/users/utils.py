from apps.api.admin.serializers import UserJWTSerializer


def jwt_response_payload_handler(token, user=None, request=None):
    user_data = UserJWTSerializer(user, context={'request': request}).data
    return {
        'user': user_data,
        'token': token,
    }
