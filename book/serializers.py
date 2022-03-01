from rest_framework import serializers
from book.models import BooksBook, BooksBookAuthors, BooksBookshelf, BooksBookLanguages,BooksBook,BooksFormat,BooksBookSubjects,BooksBookBookshelves

class BookLangSerializer(serializers.ModelSerializer):
    class Meta:
        model = BooksBookLanguages
        fields = ["language"]
        depth = 3
class BookMimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = BooksFormat
        fields =["mime_type","url"]
        depth = 3
class BookShelfSerializer(serializers.ModelSerializer):
    class Meta:
        model = BooksBookBookshelves
        fields ="__all__"
        depth = 3
class BookSubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = BooksBookSubjects
        fields ="__all__"
        depth = 3

class BookSerializer(serializers.ModelSerializer):

    language = serializers.SerializerMethodField()
    mime_type = serializers.SerializerMethodField()
    bookshelf = serializers.SerializerMethodField()
    subject = serializers.SerializerMethodField()
    

    def get_language(self,obj):
        queryset = BooksBookLanguages.objects.filter(book=obj.book)
        data =  BookLangSerializer(queryset, many=True).data
        data = [i['language'] for i in data]
        return data
    def get_mime_type(self,obj):
        queryset = BooksFormat.objects.filter(book=obj.book)
        data =  BookMimeSerializer(queryset, many=True).data
        return data
    def get_bookshelf(self,obj):
        queryset = BooksBookBookshelves.objects.filter(book=obj.book)
        data =  BookShelfSerializer(queryset, many=True).data
        data = [i['bookshelf'] for i in data]
        return data
    def get_subject(self,obj):
        queryset = BooksBookSubjects.objects.filter(book=obj.book)
        data =  BookSubjectSerializer(queryset, many=True).data
        data = [i['subject'] for i in data]
        return data
    class Meta:
        model = BooksBookAuthors
        fields = "__all__"  
        depth = 1







