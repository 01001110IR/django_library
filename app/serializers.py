from rest_framework import serializers
from .models import Book, Customer, BorrowingBook

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'  # You can specify the fields you want to include if needed

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'  

class BorrowingBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = BorrowingBook
        fields = '__all__'  
