"""myrealtrip URL Configuration
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include

urlpatterns = [
    # 항공권 페이지
    path("air",include("flight.urls")),
    # 항공권 예약 페이지
    path('air/booking', include('flight_checkout.urls')),
    # 호텔 페이지
    path('accommodations', include('hotel.urls')),
    # 호텔 예약 페이지
    path('accommodations/booking', include('hotel_booking.urls')),
    path('reviews', include('review.urls')),
    # 로그인/회원가입
    path('users', include('user.urls'))
]
