from django.core.mail import send_mail
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination, Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListCreateAPIView

from .serializers import CompanySerializer
from .models import Company


class CompanyViewSet(ModelViewSet):
    serializer_class = CompanySerializer
    queryset = Company.objects.all().order_by("-last_update")
    pagination_class = PageNumberPagination


# Create your views here.
@api_view(http_method_names=["POST"])
def send_company_email(request):
    send_mail(
        subject=request.data.get("subject"),
        message=request.data.get("message"),
        from_email="michaljazowski1995@gmail.com",
        recipient_list=["michaljazowski1995@gmail.com"],
    )
    return Response(
        {"status": "success", "info": "email sent successfully"}, status=200
    )


class CompanyPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100


class CompanyListCreateView(ListCreateAPIView):
    queryset = Company.objects.all().order_by("-last_update")
    serializer_class = CompanySerializer
    pagination_class = CompanyPagination