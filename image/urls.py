from django.urls import path
from . import views    

urlpatterns = [
    # path("hello/", views.HelloView.as_view(), name='hello'),
    path('combined/', views.ImageView.as_view()),
    path('faceswap/', views.FaceSwapView.as_view()),
]