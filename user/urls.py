from django.urls import path
from user.views import EmailSignUpView, EmailSignInView, KakaoSignInView

urlpatterns = [
    path('/signup', EmailSignUpView.as_view()),
    path('/signin', EmailSignInView.as_view()),
    path('/signin/kakao', KakaoSignInView.as_view())
]
