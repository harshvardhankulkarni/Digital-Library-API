from datetime import date

from core.models import Transaction, Student, Card
from django.db.models import Sum, Count
from django.utils.dateparse import parse_date
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serializer import BookSerializer, StudentSerializer, CardSerializer


@api_view(['GET'])
def issued_books(request):
    from_date = request.GET.get('from')
    to_date = request.GET.get('to')

    if not from_date:
        return Response({'error': 'from is required field'}, status=status.HTTP_400_BAD_REQUEST)
    if not to_date:
        return Response({'error': 'to is required field'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        from_date = parse_date(from_date)
        to_date = parse_date(to_date)
        if from_date > to_date:
            raise ValueError()
    except ValueError:
        return Response({'error': 'Invalid date format'}, status=status.HTTP_400_BAD_REQUEST)

    transactions = Transaction.objects.filter(
        transaction_date__range=(from_date, to_date), is_issued=True
    ).select_related('book')

    books = set(transaction.book for transaction in transactions)
    serializer = BookSerializer(books, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def returned_books(request):
    from_date = request.GET.get('from')
    to_date = request.GET.get('to')

    if not from_date:
        return Response({'error': 'from is required field'}, status=status.HTTP_400_BAD_REQUEST)
    if not to_date:
        return Response({'error': 'to is required field'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        from_date = parse_date(from_date)
        to_date = parse_date(to_date)
        if from_date > to_date:
            raise ValueError()
    except ValueError:
        return Response({'error': 'Invalid date format'}, status=status.HTTP_400_BAD_REQUEST)

    transactions = Transaction.objects.filter(
        transaction_date__range=(from_date, to_date), is_returned=True
    ).select_related('book')

    books = set(transaction.book for transaction in transactions)
    serializer = BookSerializer(books, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def due_books_today(request):
    transactions = Transaction.objects.filter(
        book_due_date__lte=date.today(), is_returned=False
    ).select_related('book')

    books = set(transaction.book for transaction in transactions)
    serializer = BookSerializer(books, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def total_fine(request):
    from_date = request.GET.get('from')
    to_date = request.GET.get('to')

    if not from_date:
        return Response({'error': 'from is required field'}, status=status.HTTP_400_BAD_REQUEST)
    if not to_date:
        return Response({'error': 'to is required field'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        from_date = parse_date(from_date)
        to_date = parse_date(to_date)
        if from_date > to_date:
            raise ValueError()
    except ValueError:
        return Response({'error': 'Invalid date format'}, status=status.HTTP_400_BAD_REQUEST)

    fine_amount = Transaction.objects.filter(
        transaction_date__range=(from_date, to_date)
    ).aggregate(Sum('fine_amount'))

    return Response(fine_amount)


@api_view(['GET'])
def total_student_signed_up(request):
    date_for_student = request.GET.get('date')

    if not date_for_student:
        return Response({'error': 'date is required field'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        date_for_student = parse_date(date_for_student)
    except ValueError:
        return Response({'error': 'Invalid date format'}, status=status.HTTP_400_BAD_REQUEST)

    signed_up_student = Student.objects.filter(created_on=date_for_student).count()

    return Response({
        'Total_students_signed_up': signed_up_student
    })


@api_view(['GET'])
def inactivate_card_students(request):
    students = Student.objects.filter(card=None)
    serializer = StudentSerializer(students, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def card_with_three_book_issued(request):
    transactions = Transaction.objects.filter(
        status=True, is_issued=True
    ).values('card').annotate(num_issued_books=Count('id')).filter(num_issued_books=3)

    card_ids_with_three_issued_books = transactions.values_list('card', flat=True)
    cards_with_three_issued_books = Card.objects.filter(id__in=card_ids_with_three_issued_books)

    for card in cards_with_three_issued_books:
        print(f'Card ID: {card.id}, Student Name: {card.student.name}')

    serializer = CardSerializer(cards_with_three_issued_books, many=True)
    return Response(serializer.data)
