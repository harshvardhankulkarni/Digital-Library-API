from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, SerializerMethodField
from rest_framework.validators import UniqueValidator

from ..models import Student, Book, Author, Transaction, Card


class StudentSerializer(ModelSerializer):
    name = serializers.CharField(required=True)
    age = serializers.IntegerField(required=True)
    email = serializers.EmailField(required=True, validators=[UniqueValidator(Student.objects.all())])
    phone_number = serializers.CharField(required=True, max_length=15)

    class Meta:
        model = Student
        fields = ['name', 'age', 'email', 'phone_number', 'country', 'card']


class AuthorSerializer(ModelSerializer):
    name = serializers.CharField(required=True)
    age = serializers.IntegerField(required=True)
    email = serializers.EmailField(required=True)

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
