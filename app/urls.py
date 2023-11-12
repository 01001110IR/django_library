from django.urls import path
from . import views

urlpatterns = [
    
    path("books_list/", views.book_list), 
    path("customer_list/", views.customer_list),# Add this line to create a URL for listing books
    path('borrow_book/', views.borrow_book),
    path('return_book/', views.return_book),

]
