from  django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    GetBookViewset,
)

router  = DefaultRouter(trailing_slash=False)

router.register(r"",GetBookViewset,basename="book_list") 

urlpatterns = [
    path('', include(router.urls)),
]