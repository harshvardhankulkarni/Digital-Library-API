from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from core.models import Book, Author
from .serializer import BookSerializer
from .validators import validate_email


@api_view(['GET', 'POST'])
def book_list(request):
    if request.method == 'GET':
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        author_email = request.data.get('author_email')
        author_name = request.data.get('author_name')

        if not author_email:
            return Response({'author_email': 'This field is required.'}, status=status.HTTP_400_BAD_REQUEST)

        if not author_name:
            return Response({'author_name': 'This field is required.'}, status=status.HTTP_400_BAD_REQUEST)

        if validate_email(author_email):
            return Response({'error': 'Author email is not valid.'}, status=status.HTTP_400_BAD_REQUEST)

        author, created = Author.objects.get_or_create(email=author_email)

        if created:
            author.name = author_name
            author.save()

        request.data['author'] = author.id
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def book_detail(request, pk):
    try:
        book = Book.objects.get(pk=pk)
    except Book.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = BookSerializer(book)
        return Response(serializer.data)

    elif request.method == 'PUT':
        book = BookSerializer(book, data=request.data)
        if book.is_valid():
            book.save()
            return Response(book.data)
        return Response(book.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        book.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
