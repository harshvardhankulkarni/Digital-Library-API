import os
from datetime import date, timedelta

from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, SerializerMethodField
from rest_framework.validators import UniqueValidator

from core.models import Student, Book, Author, Transaction, Card, Country


class StudentSerializer(ModelSerializer):
    name = serializers.CharField(required=True)
    age = serializers.IntegerField(required=True)
    email = serializers.EmailField(required=True, validators=[UniqueValidator(Student.objects.all())])
    phone_number = serializers.CharField(required=True, max_length=15)
    country = serializers.PrimaryKeyRelatedField(queryset=Country.objects.all())
    card = serializers.PrimaryKeyRelatedField(queryset=Card.objects.all(), allow_null=True, required=False)

    class Meta:
        model = Student
        fields = ['name', 'age', 'email', 'phone_number', 'country', 'card']

    def create(self, validated_data):
        card_validity = int(os.getenv('CARD_VALIDITY'))
        validated_data['card'] = Card.objects.create(valid_up_to=date.today() + timedelta(days=card_validity))
        return Student.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.age = validated_data.get('age', instance.age)
        instance.email = validated_data.get('email', instance.email)
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.country = validated_data.get('country', instance.country)
        instance.card = validated_data.get('card', instance.card)
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


class CardSerializer(ModelSerializer):
    student_name = SerializerMethodField()

    class Meta:
        model = Card
        fields = ['id', 'student_name']

    def get_student_name(self, obj):
        return obj.student.name if obj.student else None
