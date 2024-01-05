from core.data import scrape_genra, scrape_languages, scrape_countries
from core.models import Country, Language, Genra
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(["GET"])
def get_routes(request):
    routes = [
        "GET /api",
        # Student
        "GET /api/students",
        "POST /api/students",
        "GET /api/students/<int:id>",
        "PUT /api/students/<int:id>",
        "DEL /api/students/<int:id>",
        # Book
        "GET /api/books",
        "POST /api/books",
        "GET /api/books/<int:id>",
        "PUT /api/books/<int:id>",
        "DEL /api/books/<int:id>",
        # Author
        "GET /api/authors",
        "POST /api/authors",
        "GET /api/authors/<int:id>",
        "PUT /api/authors/<int:id>",
        "DEL /api/authors/<int:id>",
        # Transaction
        'POST /api/transaction/issue_book/',
        'POST /api/transaction/return_book/',
        'GET /api/transaction/<int:id>',
        'GET /api/transaction/books/<int:id>',
        'GET /api/transaction/cards/<int:id>',
        # Report
        'GET /api/report/books-issued/?from=<Date:date>&to=<Date:date>',
        'GET /api/report/books-returned/?from=<Date:date>&to=<Date:date>',
        'GET /api/report/total-fine/?from=<Date:date>&to=<Date:date>',
        'GET /api/report/total-signed-up-students/?date=<Date:date>',
        'GET /api/report/inactivate-card-students/',
        'GET /api/report/due-books/',
        'GET /api/report/card-with-three-book-issued/',
    ]
    return Response(routes)


@api_view(["GET"])
def need_data(request):
    exist: bool = False
    countries = Country.objects.all()
    if not countries.exists():
        for country in scrape_countries():
            Country.objects.create(country_name=country)
    else:
        exist = True

    languages = Language.objects.all()
    if not languages.exists():
        for language in scrape_languages():
            Language.objects.create(language=language)
    else:
        exist = True

    all_genra = Genra.objects.all()
    if not all_genra.exists():
        for genra in scrape_genra():
            Genra.objects.create(genra=genra)
    else:
        exist = True

    if not exist:
        return Response({
            "message": "Countries, Languages, Genra Added successfully"
        }, status=status.HTTP_200_OK)
    else:
        return Response({
            "message": "Countries, Languages, Genra Data already exists"
        }, status=status.HTTP_200_OK)
