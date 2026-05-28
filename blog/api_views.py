import logging

from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils.text import slugify
from .models import Post
from .serializers import PostSerializer
from .services import generate_blog_post

logger = logging.getLogger('blog')


"""
ListAPIView                → GET list (read only)
CreateAPIView              → POST only
ListCreateAPIView          → GET list + POST
RetrieveAPIView            → GET single object (read only)
RetrieveUpdateAPIView      → GET + PUT/PATCH
RetrieveDestroyAPIView     → GET + DELETE
RetrieveUpdateDestroyAPIView → GET + PUT/PATCH + DELETE

"""

class PostListAPI(generics.ListCreateAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = Post.objects.filter(published=True).order_by('-created_at')
        tag = self.request.query_params.get('tag')
        if tag:
            queryset = queryset.filter(tags__name=tag)
        return queryset

    def perform_create(self, serializer):
        post = serializer.save(author=self.request.user)
        logger.info('API post created: slug=%s author=%s', post.slug, self.request.user)


class PostDetailAPI(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    lookup_field = 'slug'

    def get_queryset(self):
        return Post.objects.filter(published=True)


class GeneratePostAPI(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        topic = request.data.get('topic')

        if not topic:
            logger.warning('API generate request missing topic: user=%s', request.user)
            return Response(
                {'error': 'topic is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        logger.info('API post generation started: topic=%s user=%s', topic, request.user)
        try:
            generated = generate_blog_post(topic)

            post = Post.objects.create(
                title=generated['title'],
                content=generated['content'],
                slug=slugify(generated['title']),
                author=request.user,
                published=False  # save as draft first
            )

            logger.info('API post generation succeeded: slug=%s', post.slug)
            serializer = PostSerializer(post)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            logger.exception('API post generation failed: topic=%s user=%s', topic, request.user)
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )