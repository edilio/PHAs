# Create your views here.
from django.views.generic import ListView
from django.shortcuts import render_to_response

from rest_framework import filters, viewsets, permissions
from django_filters.rest_framework import DjangoFilterBackend


from models import Pha, PROGRAM_CHOICES_WITH_ALL
from .serializers import PhaSerializer


def home(request):
    # View code here...
    return render_to_response('hudmap.html')


def section8(request):
    # View code here...
    phas = Pha.objects.filter(section8_units__gt=0)

    return render_to_response('haunits.html', {'listname': 'Section 8', 'phas': phas} )


def ph(request):
    # View code here...
    page = request.GET.get('p', '0')
    initial_record = int(page)*10
    phas = Pha.objects.filter(low_rent_units__gt=0)[initial_record:initial_record+10]

    return render_to_response('haunits.html', {'listname': 'Public Housing', 'phas': phas})


def without_website(request):
    order_by = request.GET.get('order_by', 'name')
    phas = Pha.objects.filter(web_page_address='')
    zero_units = request.GET.get('zero_units')
    if zero_units == '0':
        phas = phas.filter(total_units__gt=0)
    elif zero_units == '1':
        phas = phas.filter(total_units=0)
    program = request.GET.get('program')
    if program and program != 'All':
        phas = phas.filter(program=program)
    phas = phas.order_by(order_by)

    context = {
        'listname': 'Without Web Site',
        'phas': phas,
        'zero_units': zero_units,
        'order_by': order_by,
        'programs': PROGRAM_CHOICES_WITH_ALL,
        'program': program
    }
    return render_to_response('webless.html', context=context)


def without_email(request):
    phas = Pha.objects.filter(email_address='')

    return render_to_response('webless.html', {'listname': 'Without Email Address', 'phas': phas})


class PhaList(ListView):
    model = Pha


class PhaViewSet(viewsets.ModelViewSet):
    model = Pha
    serializer_class = PhaSerializer
    queryset = Pha.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = (filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend)
    search_fields = ('code', 'name')
    ordering_fields = ('code', 'name', 'city')
    filter_fields = ('state', 'city', 'program')
