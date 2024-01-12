from django.urls import path

from ..api import views, student, author, transaction, book, report

urlpatterns = [
    path('', views.get_routes),

    path('students/', student.StudentList.as_view()),
    path('students/<int:pk>', student.StudentDetail.as_view()),
    # path('students/', student.student_list),
    # path('students/<int:pk>', student.student_detail),

    path('authors/', author.AuthorList.as_view()),
    path('authors/<int:pk>', author.AuthorDetail.as_view()),
    # path('authors/', author.author_list),
    # path('authors/<int:pk>', author.author_detail),

    path('books/', book.book_list),
    path('books/<int:pk>', book.book_detail),

    path('transaction/issue_book/', transaction.issue_book),
    path('transaction/return_book/', transaction.return_book),
    path('transaction/books/<int:pk>', transaction.transaction_details_book),
    path('transaction/cards/<int:pk>', transaction.transaction_details_card),
    path('transaction/<int:pk>', transaction.transaction_detail),

    path('report/books-issued/', report.issued_books),
    path('report/books-returned/', report.returned_books),
    path('report/total-fine/', report.total_fine),
    path('report/total-signed-up-students/', report.total_student_signed_up),
    path('report/inactivate-card-students/', report.inactivate_card_students),
    path('report/due-books/', report.due_books_today),
    path('report/card-with-three-book-issued/', report.card_with_three_book_issued),

    path('need-data/', views.need_data)
]
