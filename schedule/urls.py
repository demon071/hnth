from django.urls import path
from . import views

urlpatterns = [
    path('', views.ConferenceListView.as_view(), name='conference_list'),
    path('create/', views.ConferenceCreateView.as_view(), name='conference_create'),
    path('<int:pk>/update/', views.ConferenceUpdateView.as_view(), name='conference_update'),
    path('<int:pk>/delete/', views.ConferenceDeleteView.as_view(), name='conference_delete'),
    
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),

    # Location URLs
    path('locations/', views.LocationListView.as_view(), name='location_list'),
    path('locations/<int:pk>/', views.LocationDetailView.as_view(), name='location_detail'),
    path('locations/create/', views.LocationCreateView.as_view(), name='location_create'),
    path('locations/<int:pk>/update/', views.LocationUpdateView.as_view(), name='location_update'),
    path('locations/<int:pk>/delete/', views.LocationDeleteView.as_view(), name='location_delete'),

    # Participant URLs
    path('participants/', views.ParticipantListView.as_view(), name='participant_list'),
    path('participants/create/', views.ParticipantCreateView.as_view(), name='participant_create'),
    path('locations/<int:location_id>/participants/add/', views.ParticipantCreateView.as_view(), name='participant_add'),
    path('participants/<int:pk>/update/', views.ParticipantUpdateView.as_view(), name='participant_update'),
    path('participants/<int:pk>/delete/', views.ParticipantDeleteView.as_view(), name='participant_delete'),

    # Search URL
    path('search/', views.ParticipantSearchView.as_view(), name='participant_search'),
]
