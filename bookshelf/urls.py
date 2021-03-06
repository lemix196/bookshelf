"""bookshelf URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include

from books.views import (
    book_list_view,
    home_view,
    book_search_view,
    book_add_view,
    book_edit_view,
    book_delete_view
    )

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view, name='home'),
    path('book-list/', book_list_view, name='book-list'),
    path('book-search/', book_search_view, name='book-search'),
    path('book-add/', book_add_view, name='book-add'),
    path('book_edit/<int:book_id>/', book_edit_view, name='book-edit'),
    path('book_delete/<int:book_id>/', book_delete_view, name='book-delete'),
    path('api/', include('api.urls')),
]
