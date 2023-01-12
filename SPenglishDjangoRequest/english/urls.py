from django.urls import path
from . import views
# 定義起始網址後需要接的網站名稱
urlpatterns = [
    path('learning', views.callback)
]