from rest_framework.permissions import IsAuthenticated, SAFE_METHODS
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from api_v1.permissions import IsOwnerOrReadOnly
from api_v1.serializers import PostSerializer
from webapp.models import Post


class PostViewSet(ModelViewSet):
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_permissions(self):
        if self.request.method in SAFE_METHODS or self.request.user.is_superuser:
            return []
        return [IsOwnerOrReadOnly()]


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        user.auth_token.delete()
        return Response({'status': 'ok'})
