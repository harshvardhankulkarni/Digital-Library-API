import os
from datetime import date, timedelta

from core.models import Student, Card
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serializer import StudentSerializer


@api_view(['GET', 'POST'])
def student_list(request):
    card_validity = int(os.getenv('CARD_VALIDITY'))
    if request.method == 'GET':
        students = Student.objects.all()
        serializer = StudentSerializer(students, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        request.data['card'] = Card.objects.create(valid_up_to=date.today() + timedelta(days=card_validity)).id
        serializer = StudentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def student_detail(request, pk):
    try:
        student = Student.objects.get(pk=pk)
    except Student.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = StudentSerializer(student)
        return Response(serializer.data)

    elif request.method == 'PUT':
        student = StudentSerializer(student, data=request.data)
        if student.is_valid():
            student.save()
            return Response(student.data)
        return Response(student.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        student.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
