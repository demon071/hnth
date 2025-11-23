from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.db.models import Count
from django.db.models.functions import TruncWeek, TruncMonth, TruncYear
from .models import Conference, Location, Participant
from .forms import ConferenceForm, LocationForm, ParticipantForm
from datetime import datetime

class ConferenceListView(LoginRequiredMixin, ListView):
    model = Conference
    template_name = 'schedule/conference_list.html'
    context_object_name = 'conferences'
    ordering = ['-start_time']

class ConferenceCreateView(LoginRequiredMixin, CreateView):
    model = Conference
    form_class = ConferenceForm
    template_name = 'schedule/conference_form.html'
    success_url = reverse_lazy('conference_list')

class ConferenceUpdateView(LoginRequiredMixin, UpdateView):
    model = Conference
    form_class = ConferenceForm
    template_name = 'schedule/conference_form.html'
    success_url = reverse_lazy('conference_list')

class ConferenceDeleteView(LoginRequiredMixin, DeleteView):
    model = Conference
    template_name = 'schedule/conference_confirm_delete.html'
    success_url = reverse_lazy('conference_list')

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'schedule/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Base QuerySet
        conferences = Conference.objects.all()

        # Date Filtering
        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')

        if start_date and end_date:
            conferences = conferences.filter(start_time__date__range=[start_date, end_date])
        
        # Basic stats
        context['total_conferences'] = conferences.count()
        
        # Format stats
        format_data = conferences.values('format').annotate(count=Count('id'))
        context['format_labels'] = [item['format'] for item in format_data]
        context['format_counts'] = [item['count'] for item in format_data]

        # Time-based stats
        filter_type = self.request.GET.get('filter', 'month')
        
        if filter_type == 'week':
            time_data = conferences.annotate(period=TruncWeek('start_time')).values('period').annotate(count=Count('id')).order_by('period')
        elif filter_type == 'year':
            time_data = conferences.annotate(period=TruncYear('start_time')).values('period').annotate(count=Count('id')).order_by('period')
        else: # month (default)
            time_data = conferences.annotate(period=TruncMonth('start_time')).values('period').annotate(count=Count('id')).order_by('period')

        context['time_labels'] = [item['period'].strftime('%Y-%m-%d') for item in time_data]
        context['time_counts'] = [item['count'] for item in time_data]
        context['filter_type'] = filter_type
        context['start_date'] = start_date
        context['end_date'] = end_date

        return context

# Location Views
class LocationListView(LoginRequiredMixin, ListView):
    model = Location
    template_name = 'schedule/location_list.html'
    context_object_name = 'locations'

class LocationDetailView(LoginRequiredMixin, DetailView):
    model = Location
    template_name = 'schedule/location_detail.html'
    context_object_name = 'location'

class LocationCreateView(LoginRequiredMixin, CreateView):
    model = Location
    form_class = LocationForm
    template_name = 'schedule/location_form.html'
    success_url = reverse_lazy('location_list')

class LocationUpdateView(LoginRequiredMixin, UpdateView):
    model = Location
    form_class = LocationForm
    template_name = 'schedule/location_form.html'
    success_url = reverse_lazy('location_list')

class LocationDeleteView(LoginRequiredMixin, DeleteView):
    model = Location
    template_name = 'schedule/conference_confirm_delete.html'
    success_url = reverse_lazy('location_list')

# Participant Views
class ParticipantListView(LoginRequiredMixin, ListView):
    model = Participant
    template_name = 'schedule/participant_list.html'
    context_object_name = 'participants'

class ParticipantCreateView(LoginRequiredMixin, CreateView):
    model = Participant
    form_class = ParticipantForm
    template_name = 'schedule/participant_form.html'
    success_url = reverse_lazy('participant_list')

    def get_initial(self):
        initial = super().get_initial()
        # If location_id is in URL, pre-select it
        location_id = self.kwargs.get('location_id')
        if location_id:
            initial['location'] = location_id
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        location_id = self.kwargs.get('location_id')
        if location_id:
            context['location'] = get_object_or_404(Location, pk=location_id)
        return context

class ParticipantUpdateView(LoginRequiredMixin, UpdateView):
    model = Participant
    form_class = ParticipantForm
    template_name = 'schedule/participant_form.html'
    success_url = reverse_lazy('participant_list')

class ParticipantDeleteView(LoginRequiredMixin, DeleteView):
    model = Participant
    template_name = 'schedule/conference_confirm_delete.html'
    success_url = reverse_lazy('participant_list')

# Search View
class ParticipantSearchView(LoginRequiredMixin, ListView):
    model = Participant
    template_name = 'schedule/participant_search.html'
    context_object_name = 'results'

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Participant.objects.filter(name__icontains=query).select_related('location')
        return Participant.objects.none()

    def render_to_response(self, context, **response_kwargs):
        # Check if this is an AJAX request
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            from django.http import JsonResponse
            results = []
            for participant in context['results']:
                results.append({
                    'name': participant.name,
                    'location_id': participant.location.pk,
                    'location_name': participant.location.name,
                    'location_address': participant.location.address or '',
                })
            return JsonResponse({'results': results})
        return super().render_to_response(context, **response_kwargs)
