import os
from datetime import date, timedelta

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from core.models import Book, Transaction, Student
from .serializer import TransactionSerializer


@api_view(['POST'])
def issue_book(request):
    if request.method == 'POST':
        book_id = request.data.get('book')
        student_id = request.data.get('student')

        # Check if the Student is Exist
        try:
            student = Student.objects.get(id=student_id)
        except Student.DoesNotExist:
            return Response({'error': 'Student not found'}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the book is Exist
        try:
            book = Book.objects.get(id=book_id)
        except Book.DoesNotExist:
            return Response({'error': 'Book not found'}, status=status.HTTP_400_BAD_REQUEST)

        # Check if book is Available
        if not book.available:
            return Response({'error': 'Book not Available'}, status=status.HTTP_400_BAD_REQUEST)

        # Check if Student don't issued 3 books
        if student.issued_books >= 3:
            return Response({'error': 'Student has reached the maximum number of issued books'},
                            status=status.HTTP_400_BAD_REQUEST)

        today_date = date.today()
        book_due_date = today_date - timedelta(days=int(os.getenv('BOOK_VALIDITY')))

        # Issue the book
        transaction = Transaction.objects.create(
            student=student, book=book, is_issued=True, is_returned=False, status=True,
            book_due_date=book_due_date)

        # Issued One Book Student
        student.issued_books += 1
        student.save()

        # Book is Now unavailable
        book.available = False
        book.save()

        return Response({
            'message': 'Book Issued Successfully',
            'due_date': transaction.book_due_date.strftime('%Y-%m-%d')
        })


@api_view(['POST'])
def return_book(request):
    fine = int(os.getenv('FINE'))
    if request.method == 'POST':
        book_id = request.data.get('book')
        student_id = request.data.get('student')

        fine_amount: int = 0

        try:
            student = Student.objects.get(id=student_id)
        except Student.DoesNotExist:
            return Response({'error': 'Student not found'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            book = Book.objects.get(id=book_id)
        except Book.DoesNotExist:
            return Response({'error': 'Book not found'}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the transaction is available
        try:
            transaction = Transaction.objects.get(book=book, student=student, status=True)
        except Transaction.DoesNotExist:
            return Response({'error': 'Transaction not found'}, status=status.HTTP_400_BAD_REQUEST)

        # Book is Now available
        book.available = True
        book.save()
        today = date.today()

        if today > transaction.book_due_date:
            fine_amount = (today - transaction.book_due_date) * fine

        # update student
        student.issued_books -= 1
        student.save()

        # Update Transaction Details
        transaction.fine_amount = fine_amount
        transaction.is_returned = True
        transaction.status = False
        transaction.save()

        return Response({
            'message': 'Book Returned Successfully',
            'fine': fine_amount
        })


@api_view(['GET'])
def transaction_details_book(request, pk):
    try:
        book = Book.objects.get(id=pk)
    except Book.DoesNotExist:
        return Response({'error': 'Book not found'}, status=status.HTTP_400_BAD_REQUEST)

    transactions = Transaction.objects.filter(book=book)
    serializer = TransactionSerializer(transactions, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def transaction_details_student(request, pk):
    try:
        student = Student.objects.get(id=pk)
    except Student.DoesNotExist:
        return Response({'error': 'Student not found'}, status=status.HTTP_400_BAD_REQUEST)

    transactions = Transaction.objects.filter(student=student)
    serializer = TransactionSerializer(transactions, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def transaction_detail(request, pk):
    try:
        transaction = Transaction.objects.get(pk=pk)
    except Transaction.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = TransactionSerializer(transaction)
    return Response(serializer.data)
