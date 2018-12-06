from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    path('stats/', views.TotalStats.as_view()),
    path('stats/<author>', views.author_stats),
    path('authors/', views.AuthorList.as_view())
]

urlpatterns = format_suffix_patterns(urlpatterns)
