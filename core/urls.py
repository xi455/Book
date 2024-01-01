"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from app import views as app_views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("signup/", app_views.BorrowerCreateView.as_view(), name="signup"),
    path("", app_views.BookListItem.as_view(), name="book-list"),
    path("book/<pk>/detail/", app_views.BookDetailView.as_view(), name="book-detail"),
    path("book/create/", app_views.BookCreateView.as_view(), name="book-create"),
    path("book/<pk>/update/", app_views.BookUpdateView.as_view(), name="book-update"),
    path("book/<pk>/delete/", app_views.book_delete, name="book-delete"),
    path("book/logs/", app_views.RecordLendListItem.as_view(), name="book-logs"),
    path("borrower/", app_views.BorrowerListItem.as_view(), name="borrower-list"),
    path(
        "borrower/<pk>/detail/",
        app_views.BorrowerDetailView.as_view(),
        name="borrower-detail",
    ),
    path(
        "borrower/<pk>/update/",
        app_views.BorrowerUpdateView.as_view(),
        name="borrower-update",
    ),
    path(
        "record/create/",
        app_views.RecordCreateView.as_view(),
        name="record-create",
    ),
    path(
        "record/time-out/",
        app_views.RecordTimeOutListView.as_view(),
        name="record-time-out",
    ),
    path(
        "record/<pk>/update/",
        app_views.RecordUpdateView.as_view(),
        name="record-update",
    ),
]

urlpatterns += static(
    settings.STATIC_URL,
    document_root=settings.STATIC_ROOT,
)
urlpatterns += static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT,
)
