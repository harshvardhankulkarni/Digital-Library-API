from ..models import Student, Book, Author, Transaction, Card
from rest_framework.serializers import ModelSerializer, SerializerMethodField


class StudentSerializer(ModelSerializer):
    class Meta:
        model = Student
        fields = ['name', 'age', 'email', 'phone_number', 'country', 'card']


class AuthorSerializer(ModelSerializer):
    class Meta:
        model = Author
        fields = ['name', 'age', 'email', 'country']


class BookSerializer(ModelSerializer):
    class Meta:
        model = Book
        fields = ['name', 'author', 'number_of_pages', 'language', 'available', 'genra', 'ISBN_number',
                  'published_date']


class TransactionSerializer(ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['card', 'book', 'book_due_date', 'is_issued', 'is_returned', 'fine_amount', 'status']


class CardSerializer(ModelSerializer):
    student_name = SerializerMethodField()

    class Meta:
        model = Card
        fields = ['id', 'student_name']

    def get_student_name(self, obj):
        return obj.student.name if obj.student else None
