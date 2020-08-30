from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication


class AuthRequiredMixin(object):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    # Base class for token based authentication
