import os
from datetime import date

from core.models import Book, Transaction, Card, Student
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serializer import TransactionSerializer


@api_view(['POST'])
def issue_book(request):
    if request.method == 'POST':
        book_id = request.data.get('book')
        card_id = request.data.get('card')

        # Check if the card is active
        try:
            card = Card.objects.get(id=card_id)
            if not card.valid_up_to >= date.today():
                card.status = False
                card.save()
                return Response({'error': 'Card not active'}, status=status.HTTP_400_BAD_REQUEST)
            try:
                card.student
            except Student.DoesNotExist:
                return Response({'error': 'Card has no student'}, status=status.HTTP_400_BAD_REQUEST)
        except Card.DoesNotExist:
            return Response({'error': 'Card not found'}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the book is available
        try:
            book = Book.objects.get(id=book_id, available=True)
        except Book.DoesNotExist:
            return Response({'error': 'Book not found or not available'}, status=status.HTTP_400_BAD_REQUEST)

        if Transaction.objects.filter(card=card, status=True).count() >= 3:
            return Response({'error': 'Card has reached the maximum number of issued books'},
                            status=status.HTTP_400_BAD_REQUEST)

        # Issue the book
        transaction = Transaction.objects.create(card=card, book=book, is_issued=True, is_returned=False, status=True,
                                                 book_due_date=card.valid_up_to)

        # Book is Now unavailable
        book.available = False
        book.save()

        return Response({
            'message': 'Book Issued Successfully',
            'due_date': card.valid_up_to.strftime('%Y-%m-%d')
        })


@api_view(['POST'])
def return_book(request):
    fine = int(os.getenv('FINE'))
    if request.method == 'POST':
        book_id = request.data.get('book')
        card_id = request.data.get('card')

        fine_amount: int = 0

        try:
            card = Card.objects.get(id=card_id)
        except Card.DoesNotExist:
            return Response({'error': 'Card not found'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            book = Book.objects.get(id=book_id)
        except Book.DoesNotExist:
            return Response({'error': 'Book not found'}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the transaction is available
        try:
            transaction = Transaction.objects.get(book=book, card=card, status=True)
        except Transaction.DoesNotExist:
            return Response({'error': 'Transaction not found'}, status=status.HTTP_400_BAD_REQUEST)

        if card.status:
            # Book is Now available
            book.available = True
            book.save()

            if date.today() > transaction.book_due_date:
                fine_amount = (date.today() - transaction.book_due_date) * fine

                # Deactivate card
                card.status = False
                card.save()

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
def transaction_details_card(request, pk):
    try:
        card = Card.objects.get(id=pk)
    except Card.DoesNotExist:
        return Response({'error': 'Card not found'}, status=status.HTTP_400_BAD_REQUEST)

    transactions = Transaction.objects.filter(card=card)
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
