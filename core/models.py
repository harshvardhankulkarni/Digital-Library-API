from django.db import models


class Country(models.Model):
    country_name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return f'{self.country_name}'


class Language(models.Model):
    language = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return f'{self.language}'


class Genra(models.Model):
    genra = models.CharField(null=False, max_length=255, unique=True)

    def __str__(self):
        return f'{self.genra}'


class Author(models.Model):
    name = models.CharField(null=False, max_length=255)
    email = models.EmailField(null=False, max_length=255, unique=True)
    age = models.IntegerField(null=True, blank=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f'{self.name}'


class Book(models.Model):
    name = models.CharField(null=False, max_length=255, unique=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    number_of_pages = models.BigIntegerField(null=False)
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    available = models.BooleanField(null=False, default=True)
    genra = models.ForeignKey(Genra, on_delete=models.CASCADE)
    ISBN_number = models.UUIDField()
    published_date = models.DateField()

    def __str__(self):
        return f'{self.name}'


class Student(models.Model):
    name = models.CharField(null=False, max_length=255)
    age = models.IntegerField(null=False)
    email = models.EmailField(null=False, max_length=255, unique=True)
    phone_number = models.CharField(max_length=15, null=False)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    created_on = models.DateField(auto_now_add=True)
    updated_on = models.DateField(auto_now=True)
    issued_books = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.name}'


class Transaction(models.Model):
    student = models.ForeignKey(Student, on_delete=models.SET_NULL, null=True, blank=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    transaction_date = models.DateField(auto_now_add=True)
    book_due_date = models.DateField()
    is_issued = models.BooleanField(null=False)
    is_returned = models.BooleanField(null=False)
    fine_amount = models.IntegerField(default=0)
    status = models.BooleanField(null=False, default=True)
    created_on = models.DateField(auto_now_add=True)
    updated_on = models.DateField(auto_now=True)

    def __str__(self):
        return f'{self.student}" - "{self.book}'
