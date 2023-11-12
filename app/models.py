

from django.utils import timezone

from django.db import models

class Book(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    author = models.CharField(max_length=50)
    year_published = models.IntegerField()
    
    # Provide a default value for received_in
    received_in = models.DateTimeField(default=timezone.now, blank=True)
    
    active = models.BooleanField(default=True)

# Rest of your models and code...


class Customer (models.Model):
      id = models.AutoField(primary_key=True)
      full_name = models.CharField(max_length=50)
      email = models.EmailField(max_length=100)
      phone_number = models.CharField(max_length=20)
      active = models.BooleanField(default=True)
      borrowed_books = models.ManyToManyField(Book, through='BorrowingBook')

      
      
      
class BorrowingBook(models.Model):
    id = models.AutoField(primary_key=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    borrowed_date = models.DateTimeField(default=timezone.now, blank=True)
    returned_date = models.DateTimeField(null=True, blank=True)
    
    
    
    
    
# {
#     "name": "test",
#     "author": "nir",
#     "year_published": 2023
# }



# {
#     "full_name": "John Doe",
#     "email": "johndoe@example.com",
#     "phone_number": "123-456-7890",
#     "active": true
# }


# {
#   "book": 1,
#   "customer": 1
# }
