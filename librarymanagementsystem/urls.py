"""librarymanagementsystem URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path
from libsystem import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('admin/', admin.site.urls),
    path('author/', csrf_exempt(views.AuthorView.as_view())),
    # path('author/<int:id>', csrf_exempt(views.AuthorView.as_view())),
    path('language/',csrf_exempt(views.LanguageView.as_view())),
    # path('language/<int:id>', csrf_exempt(views.LanguageView.as_view())),
    path('publisher/', csrf_exempt(views.PublisherView.as_view())),
    path('publisher/<int:id>', csrf_exempt(views.PublisherView.as_view())),
    path('book/', csrf_exempt(views.BookView.as_view())),
    path('book/<int:id>', csrf_exempt(views.BookView.as_view())),
    path('ebook/', csrf_exempt(views.EbookView.as_view())),
    path('ebook/<int:id>', csrf_exempt(views.EbookView.as_view())),
    path('user/', csrf_exempt(views.UserView.as_view())),
    path('user/<int:id>', csrf_exempt(views.UserView.as_view())),
    path('hardcopy/', csrf_exempt(views.HardCopyView.as_view())),
    path('hardcopy/<int:id>', csrf_exempt(views.HardCopyView.as_view())),
    # path('search/', csrf_exempt(views.Search.as_view())),   
]
