from django.urls import path, include
from . import views

app_name = 'home'

urlpatterns = [
    path('',views.Home.as_view(), name='home'),
    path('tow/<int:id>/<str:name>/',views.Tow.as_view(),name='tow'),

    # path('<int:pk>/',views.CarDetail.as_view(),name='Car_Detail'),
    # path('<slug:my_slug>/',views.CarDetail.as_view(),name='Car_Detail'),
    path('<int:year>/<str:name>/<str:owner>/',views.CarDetail.as_view(),name='Car_Detail'),

    path('creat/',views.CreateCarView.as_view(),name='create_car'),# form view
    path('creat2/',views.CreateCarView2.as_view(),name='create_car2'),#create view
    path('delete/<int:pk>/',views.CarDelete.as_view(),name='delete_Car'),
    path('Update/<int:pk>/',views.CarUpdate.as_view(),name='Update_Car'),

    path('login/',views.UserLogin.as_view(),name='login'),
    path('Logout/',views.UserLogout.as_view(),name='logout'),

    path('<int:year>/<int:month>/',views.MonthCar.as_view(),name='a'),
    # path('<int:year>/<str:month>/',views.MonthCar.as_view(),name='a'),
#===================================================================================================
    path('home2/',views.Home2.as_view()),
    path('SingleCar/<int:pk>/',views.SingleCar.as_view()),
  #  path('SingleCar/<str:name>/',views.SingleCar.as_view()),

    path('delete/<int:pk>/',views.CarDeleteAPI.as_view()),

    path('create/',views.CarCreateAPI.as_view()),
    path('update/<int:pk>/',views.CarUpdateAPI.as_view()),

    path('Createlist/',views.CarListCreateAPI.as_view()),

    path('<int:pk>/',views.Home3.as_view()),

]

