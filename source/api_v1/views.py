from rest_framework import status
from rest_framework.generics import get_object_or_404
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


class LikeToggleView(APIView):
    def post(self, request, *args, pk, action, **kwargs):
        post = get_object_or_404(Post, pk=pk)
        user = request.user
        if action == "like":
            if not post.like_users.filter(pk=user.pk).exists():
                post.like_users.add(user)
                return Response({'likes_count': post.like_users.count()})
            return Response({'detail': 'You have already liked this post.'}, status=status.HTTP_400_BAD_REQUEST)

        elif action == "unlike":
            if post.like_users.filter(pk=user.pk).exists():
                post.like_users.remove(user)
                return Response({'likes_count': post.like_users.count()})
            return Response({'detail': 'You have not liked this post yet.'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'detail': 'Invalid action'}, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        user.auth_token.delete()
        return Response({'status': 'ok'})
