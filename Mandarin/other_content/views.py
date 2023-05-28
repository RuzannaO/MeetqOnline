from django.shortcuts import render
from .models import *
from .forms import ContactUsMassageForm
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.views.generic import (
    ListView,
    DetailView,
    TemplateView
)


class EventsListView(ListView):
    model = Event
    context_object_name = 'events'
    template_name = 'other_content/events_list.html'

    def get_queryset(self):
        data = Event.objects.all()
        return data

class NewsListView(ListView):
    model = News
    context_object_name = 'news'
    template_name = 'other_content/news_list.html'

    def get_queryset(self):
        data = News.objects.all()
        return data


class EventDetailView(DetailView):
    model = Event
    context_object_name = 'event'

    def get_context_data(self, **kwargs):
        context = super(EventDetailView, self).get_context_data(**kwargs)
        context['event'] = self.object
        return context

class NewsDetailView(DetailView):
    model = News
    context_object_name = 'news'

    def get_context_data(self, **kwargs):
        context = super(NewsDetailView, self).get_context_data(**kwargs)
        context['news'] = self.object
        return context


class AboutUsView(TemplateView):
    model = Course
    context_object_name = 'about'
    template_name = 'other_content/about.html'

class ContactUsView(TemplateView):
    model = Course
    context_object_name = 'contact'
    template_name = 'other_content/contact.html'


def contactUsMassage(request):
    if request.method =='POST':
        form = ContactUsMassageForm(request.POST)
        if form.is_valid():
            data = ContactUsMassage()
            data.full_name = form.cleaned_data['full_name']
            data.email = form.cleaned_data['email']
            data.phone_number = form.cleaned_data['phone_number']
            data.massage_text = form.cleaned_data['massage_text']
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()
            messages.success(request,"Your massage has been sent! We will get touch with you!")
            return HttpResponseRedirect('/courses')

    return render(request,'home')