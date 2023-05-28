from django.urls import path
from . import views
from .views import (
    EventsListView,
    NewsListView,
    EventDetailView,
    NewsDetailView,
    AboutUsView,
    ContactUsView
)

urlpatterns = [
    path('events/', EventsListView.as_view(), name='events_list'),
    path('news/', NewsListView.as_view(), name='news_list'),
    path('event/<int:pk>/', EventDetailView.as_view(), name='event_detail'),
    path('news/<int:pk>/', NewsDetailView.as_view(), name='news_detail'),
    path('about_us/', AboutUsView.as_view(), name='about_us'),
    path('contact_us/', ContactUsView.as_view(), name='contact_us'),
    path('contact_us_massage/', views.contactUsMassage, name='contactUsMassage')
]