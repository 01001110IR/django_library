python -m venv venv  
source venv/bin/activate
pip freeze => requierments.txt
pip install django 
pip install djangorestframework
pip install pillow
pip install djangorestframework-simplejwt
pip install djangorestframework-jwt
pip install django-cors-headers
pip install PyJWT
pip install pytz
pip install markdown 
pip install django-filter

# python manage.py createsuperuser


https://www.django-rest-framework.org/

## creating a new django project :
django-admin startproject project .     <<<-  importent DOT (.)

##  run the server :
python manage.py runserver 

# Add the Pages App : 
python manage.py startapp pages

#   INSTALLED APP --- add the pages app to settings 
INSTALLED_APPS = [
    "pages.apps.PagesConfig",
     'rest_framework',
    'rest_framework_simplejwt.token_blacklist'
]
# rest_framework settings ==>

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
 
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    )
}


SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=25),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=90),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'UPDATE_LAST_LOGIN': False,
 
    'ALGORITHM': 'HS256',
    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': None,
    'JWK_URL': None,
    'LEEWAY': 0,
 
    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'USER_AUTHENTICATION_RULE': 'rest_framework_simplejwt.authentication.default_user_authentication_rule',
 
    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
 
    'JTI_CLAIM': 'jti',
 
    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': timedelta(minutes=5),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
}

# in setting for imeg ==> 
STATIC_URL = '/static/'
MEDIA_URL = '/images/'


STATICFILES_DIRS = [
    BASE_DIR / 'static',
   ]




MEDIA_ROOT = BASE_DIR / 'static/images'
STATIC_ROOT = BASE_DIR / 'staticfiles'
# At the end of setting.py add
CORS_ALLOW_ALL_ORIGINS = True

#  in the personal_portfolio/urls.py
from django.urls import path, include

path("", include("pages.urls")),

# touch pages/urls.p ==>>> createing urls file to Pages

#  in pages/urls.py
from django.urls import path
from pages import views

urlpatterns = [
    path("", views.home, name='home'),
]

# TEST = views.py =



# creating or updating database models
 python manage.py makemigrations projects
 python manage.py migrate projects




from rest_framework.response import Response
from datetime import timedelta
from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse, HttpResponse
from rest_framework import serializers
from .serializer import ProductSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated





# moduls : 
Django==4.0.6
django-cors-headers==3.13.0
djangorestframework==3.13.1
djangorestframework-jwt==1.11.0
djangorestframework-simplejwt==5.2.0
PyJWT==1.7.1
pytz==2022.1
sqlparse==0.4.2
Pillow==9.2.0


# class for example for token 
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)


        # Add custom claims
        token['username'] = user.username
        # ...


        return token




class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getNotes(request):
	return “i’m protected”


# @api_view =>> 
@api_view(['GET','POST'])
def students(request):
    if request.method == 'GET':
        tempAr=[]
        for stu in Student.objects.all():
            tempAr.append({"age":stu.age,"name":stu.sName,"id":stu.id})
        return Response(tempAr)
    elif request.method == 'POST':
        Student.objects.create(sName=request.data["name"],age=request.data["age"])
        return Response(f"student added{request.data['name']}")      

# urls for example with token  ==>> 
path('login/', views.MyTokenObtainPairView.as_view()),        