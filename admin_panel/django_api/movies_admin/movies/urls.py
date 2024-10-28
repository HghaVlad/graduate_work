from django.urls import path
from django.contrib import admin
from crud_app.views import *
from .views import say_hello

urlpatterns = [
    path('', say_hello, name='say_hello'),
    path('admin/', admin.site.urls),
    path('create/', create_view),
    path('update/<int:id>/', update_view),
    path('delete/<int:id>/', delete_view),
]
