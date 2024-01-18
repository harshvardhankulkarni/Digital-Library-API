from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from rest_framework.validators import UniqueValidator

from core.models import Student, Book, Author, Transaction, Country


class StudentSerializer(ModelSerializer):
    name = serializers.CharField(required=True)
    age = serializers.IntegerField(required=True)
    email = serializers.EmailField(required=True, validators=[UniqueValidator(Student.objects.all())])
    phone_number = serializers.CharField(required=True, max_length=15)
    country = serializers.PrimaryKeyRelatedField(queryset=Country.objects.all())
    issued_books = serializers.IntegerField(read_only=True)

    class Meta:
        model = Student
        fields = ['name', 'age', 'email', 'phone_number', 'country', 'issued_books']

    def create(self, validated_data):
        return Student.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.age = validated_data.get('age', instance.age)
        instance.email = validated_data.get('email', instance.email)
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.country = validated_data.get('country', instance.country)
        instance.save()
        return instance


class AuthorSerializer(ModelSerializer):
    name = serializers.CharField(required=True)
    age = serializers.IntegerField(required=True)
    email = serializers.EmailField(required=True)
    country = serializers.PrimaryKeyRelatedField(queryset=Country.objects.all())

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
