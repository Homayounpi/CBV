from typing import Any
from django.db import models
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView,RedirectView,DetailView,ListView,FormView,CreateView,\
            DeleteView,UpdateView,MonthArchiveView
        
from .forms import CarCreateForm
from .models import Car 
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth import views as auth_views

#=================================================================================================
from rest_framework.generics import ListAPIView,RetrieveAPIView,DestroyAPIView,CreateAPIView,UpdateAPIView,\
        ListCreateAPIView,GenericAPIView
from .serializers import CarSerializer
from rest_framework.response import Response
from rest_framework.mixins import RetrieveModelMixin,DestroyModelMixin

# class Home(View):
#     http_method_names = ['get','options','post']
#     def get(self, request):
#         return render(request, 'home/home.html')
#     def options(self, request, *args, **kwargs):
#         response = super().options(request, *args, **kwargs)
#         response.headers['host'] = 'lockal Host'
#         response.headers['user'] = request.user
#         return response
#     def http_method_not_allowed(self, request , *args, **kwargs):
#         return render(request,'method_not_allowed.html')

#===================================================================================================

# class Home(TemplateView):
#     template_name = 'home/home.html'
#     def get_context_data(self, **kwargs) :
#         context =  super().get_context_data(**kwargs)
#         context['cars'] = Car.objects.all()
#         return context
#     def post(self,request):
#         return render('home:home.html')
    
class Home(ListView):
    template_name = 'home/home.html'
    # model = Car #objects_list
    # queryset  = Car.objects.filter(year__gte=2000)
    context_object_name = 'cars'
    ordering = 'year'   #  '-year'
    def get_queryset(self) :
        result = Car.objects.filter(year__gte=2000)
        return result
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['username'] = 'homayoun'
        return context
#===================================================================================================


class Tow(RedirectView):
    # pattern_name = 'home:home' 
    url = 'home/%(id)i/%(name)s'
    query_string = True
    def get_redirect_url(self, *args, **kwargs):
        print('='*100)
        print('Hi Homayoun')
        print(kwargs['name'])
        print(kwargs['id'])
        # kwargs.pop('name')
        # kwargs.pop('id')
        return super().get_redirect_url(*args, **kwargs)
    
class Tow2(RedirectView):
    pattern_name = 'home:home' 
    # url = 'home/%(id)i/%(name)s'
    query_string = True
    def get_redirect_url(self, *args, **kwargs):
        kwargs.pop('name')
        kwargs.pop('id')
        return super().get_redirect_url(*args, **kwargs)   

#===================================================================================================

# class CarDetail(DetailView):
#     template_name = 'home/detail.html'
#     # model = Car
#     context_object_name = 'car'
#     slug_field = 'name'
#     slug_url_kwarg = 'my_slug'
#     queryset = Car.objects.filter(year__gte=2021)
#     def get_queryset(self):
#         if self.request.user.is_authenticated:
#            return Car.objects.filter(name=self.kwargs['my_slug'])
#         Car.objects.none()

class CarDetail(DetailView):
    template_name = 'home/detail.html'
    def get_object(self, queryset=None):
        return Car.objects.get(
            year=self.kwargs['year'],
            name=self.kwargs['name'],
            owner=self.kwargs['owner']
        )
 #===================================================================================================
       

class CreateCarView(FormView):
    template_name = 'home/create.html'
    form_class = CarCreateForm
    # success_url = reverse_lazy('hoasdaddame:asadhome')
    success_url = reverse_lazy('home:home')


    def form_valid(self, form):
        self._create_car(form.cleaned_data)
        messages.success(self.request,'create car !!! ','success')
        return super().form_valid(form)


    def _create_car(self,data):
        Car.objects.create(name=data['name'],year=data['year'],owner=data['owner'])
    


class CreateCarView2(CreateView):

    model = Car
    fields = ['name','year']
    template_name = 'home/create.html'
    success_url = reverse_lazy('home:home')

    def form_valid(self, form):
        car = form.save(commit=False)
        car.owner = self.request.user.username if self.request.user.username else 'root'
        car.save()
        return super().form_valid(form)
    
class CarDelete(DeleteView):
    model = Car
    success_url = reverse_lazy('home:home')
    template_name = 'home/delete.html'


class CarUpdate(UpdateView):
    model = Car
    fields = '__all__'
    success_url = reverse_lazy('home:home')
    template_name = 'home/update.html'

class UserLogin(auth_views.LoginView):
    template_name = 'home/login.html'
    next_page = reverse_lazy('home:home')

class UserLogout(auth_views.LogoutView):
    next_page = reverse_lazy('home:home')


class MonthCar(MonthArchiveView):
    model = Car
    date_field = 'created'
    template_name = 'home/home.html'
    context_object_name = 'cars'
    month_format = '%m'# agar format be surat str bashe in lazem nis benevisim

#===================================================================================================
#===================================================================================================
#API

class Home2(ListAPIView):
    serializer_class = CarSerializer
    queryset = Car.objects.all()


class SingleCar(RetrieveAPIView):
    serializer_class = CarSerializer
    queryset = Car.objects.filter()
    lookup_field = 'name'



class CarDeleteAPI(DestroyAPIView):
    serializer_class = CarSerializer
    queryset = Car.objects.all()

class CarCreateAPI(CreateAPIView):
    serializer_class = CarSerializer
    queryset = Car.objects.all()

class CarUpdateAPI(UpdateAPIView):
    serializer_class = CarSerializer
    queryset = Car.objects.all()

class CarListCreateAPI(ListCreateAPIView):
    serializer_class = CarSerializer
    queryset = Car.objects.all()


class Home3(RetrieveModelMixin,DestroyModelMixin,GenericAPIView):
    queryset = Car.objects.all()
    serializer_class = CarSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.name == 'Benz':
            return Response('Sorry')
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
      

    # def get(self,request,*args,**kwargs):
    #     instance = self.get_object()
    #     ser_data = self.get_serializer(instance).data
    #     return Response(ser_data)

    def get(self,request,*args,**kwargs):
        return self.retrieve(request,*args,**kwargs)
    def delete(self,request,*args,**kwargs):
        return self.destroy(self,request,*args,**kwargs)

