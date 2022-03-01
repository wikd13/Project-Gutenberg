from django.db.models import indexes
from rest_framework import viewsets, status
from rest_framework.response import Response
from django.db.models.functions import Lower
from django.db.models import Q
from utils.pagination import CustomPageNumberPagination
from .models import BooksBook,BooksBookAuthors,BooksBookBookshelves, BooksBookLanguages,BooksBookSubjects
from django.core.exceptions import ObjectDoesNotExist
from .serializers import (
    BookSerializer,
    BookShelfSerializer,
    BookLangSerializer,BookSerializer
)




class GetBookViewset(viewsets.ModelViewSet):
    """
    This api is used to get the list of books which satisfy the filters.    
    
    """
    serializer_class = BookSerializer
    pagination_class = CustomPageNumberPagination

    def list(self, request, *args, **kwargs):

        author_name = request.query_params.get('author_name', None)
        author_name = author_name.split(",")
        author_name = list(filter(None, author_name))

        title = request.query_params.get('title', None)
        title = title.split(",")
        title = list(filter(None, title))

        topic = request.query_params.get('topic', "")
        topic = topic.split(",")
        topic = list(filter(None, topic))

        language = request.query_params.get('language', "")
        language = language.split(",")
        language = list(filter(None, language))

        mime_type = request.query_params.get('mime_type', "")
        mime_type = mime_type.split(",")
        mime_type = list(filter(None, mime_type))

        gutenberg_id = request.query_params.get('gutenberg_id', "")
        gutenberg_id = gutenberg_id.split(",")
        gutenberg_id = list(filter(None, gutenberg_id))

        if author_name:
            q = Q()
            for a in author_name:
                q = q | Q(author__name__icontains=a)
            queryset = BooksBookAuthors.objects.filter(q).order_by('-book__download_count')
        else:
            queryset = BooksBookAuthors.objects.all().order_by('-book__download_count')

        if title:
            q = Q()
            for a in title:
                q = q | Q(book__title__icontains=a)
            queryset = queryset.filter(q)

        if gutenberg_id:
            queryset = queryset.filter(book__gutenberg_id__in=gutenberg_id)

        if language:
            q = Q()
            for a in language:
                q = q | Q(book__booksbooklanguages__language__code__iexact=a)
            queryset = queryset.filter(q)

        if topic:
            q = Q()
            for t in topic:
                q = q | Q(book__booksbookbookshelves__bookshelf__name__iexact=t) | Q(book__booksbooksubjects__subject__name__iexact=t)
            queryset = queryset.filter(q)

        if mime_type:
            queryset = queryset.filter(book__booksformat__mime_type__in=mime_type)
        count = queryset.count()
        page = self.paginate_queryset(queryset)
        book_seri = BookSerializer(page, many=True)
        return Response({"code": status.HTTP_200_OK,"total_count": count,"data": book_seri.data}, status = status.HTTP_200_OK )
