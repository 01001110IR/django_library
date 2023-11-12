from datetime import timezone
import datetime
from django.shortcuts import get_object_or_404, render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from app.models import Book, BorrowingBook, Customer
from app.serializers import BookSerializer, BorrowingBookSerializer, CustomerSerializer

@api_view(["GET", "POST"])
def book_list(request):
    if request.method == "GET":
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)  # Serialize the queryset
        return Response(serializer.data)

    elif request.method == "POST":
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            saved_book = serializer.save()
            print(f"New book added: {saved_book.name}")  # Print book name

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
@api_view(["GET", "POST"])
def customer_list(request):
    if request.method == "GET":
        customers = Customer.objects.all()
        serializer = CustomerSerializer(customers, many=True)  # Serialize the queryset
        return Response(serializer.data)

    elif request.method == "POST":
        serializer = CustomerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST", "GET"])
def borrow_book(request):
    if request.method == "GET":
        # Get a list of all borrowed books
        borrowed_books = BorrowingBook.objects.filter(returned_date__isnull=True)
        serializer = BorrowingBookSerializer(borrowed_books, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == "POST":
        # Create a new book borrowing entry
        serializer = BorrowingBookSerializer(data=request.data)
        if serializer.is_valid():
            customer_id = request.data.get('customer')
            book_id = request.data.get('book')

            # Check if the customer and book exist
            customer = get_object_or_404(Customer, pk=customer_id)
            book = get_object_or_404(Book, pk=book_id)

            # Check if the book is available to borrow
            if not book.active:
                return Response({"message": "This book is not available for borrowing."},
                                status=status.HTTP_400_BAD_REQUEST)

            # Create a new borrowing record
            borrowing = serializer.save()
            print(f"Book borrowed: {book.name} by {customer.full_name}, Borrowing ID: {borrowing.id}")
            

            # Update book availability
            book.active = False
            book.save()

            return Response({"message": "Book borrowed successfully."},
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["POST", "GET"])
def return_book(request):
    if request.method == "GET":
        # Get a list of all returned books
        returned_books = BorrowingBook.objects.filter(returned_date__isnull=False)
        serializer = BorrowingBookSerializer(returned_books, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


    elif request.method == "POST":
        # Return a borrowed book
        serializer = BorrowingBookSerializer(data=request.data)
        if serializer.is_valid():
            customer_id = request.data.get('customer')
            book_id = request.data.get('book')

            # Check if the customer and book exist
            customer = get_object_or_404(Customer, pk=customer_id)
            book = get_object_or_404(Book, pk=book_id)

            # Find the borrowing record
            try:
                borrowing = BorrowingBook.objects.get(customer=customer, book=book, returned_date__isnull=True)
            except BorrowingBook.DoesNotExist:
                return Response({"message": "No active borrowing record found for this book and customer."},
                                status=status.HTTP_404_NOT_FOUND)

            # Mark the book as returned
            borrowing.returned_date = datetime.datetime.now(timezone.utc)
            borrowing.save()
            print(f"Book returned: {book.name} by {customer.full_name}, Borrowing ID: {borrowing.id}")


            # Update book availability
            book.active = True
            book.save()

            return Response({"message": "Book returned successfully."},
                            status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)