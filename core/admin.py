from django.contrib import admin

from .models import Author, Student, Book, Country, Language, Genra, Transaction


class LanguageAdmin(admin.ModelAdmin):
    list_display = ['language']
    ordering = ['language']


admin.site.register(Language, LanguageAdmin)


class CountryAdmin(admin.ModelAdmin):
    list_display = ['country_name']
    ordering = ['country_name']


admin.site.register(Country, CountryAdmin)


class GenraAdmin(admin.ModelAdmin):
    list_display = ['genra']
    ordering = ['genra']


admin.site.register(Genra, GenraAdmin)


class AuthorAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'age', 'country']


admin.site.register(Author, AuthorAdmin)


class StudentAdmin(admin.ModelAdmin):
    list_display = ['name', 'age', 'email', 'phone_number', 'country', 'created_on', 'updated_on', 'issued_books']


admin.site.register(Student, StudentAdmin)


class BookAdmin(admin.ModelAdmin):
    list_display = ['name', 'author', 'number_of_pages', 'language', 'available', 'published_date']


admin.site.register(Book, BookAdmin)


class TransactionAdmin(admin.ModelAdmin):
    list_display = ['student', 'book', 'transaction_date', 'book_due_date', 'is_issued', 'is_returned', 'fine_amount',
                    'status']
    ordering = ['transaction_date']


admin.site.register(Transaction, TransactionAdmin)
