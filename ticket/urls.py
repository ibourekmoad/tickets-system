from django.urls import path

from ticket import views

urlpatterns = [
    path('create-ticket/', views.create_ticket, name='create_ticket'),
    path('customer-active-ticket/', views.customer_active_ticket, name='customer-active-ticket'),
    path('customer-resolved-ticket/', views.customer_resolved_ticket, name='customer-resolved-ticket'),
    path('engineer-active-ticket/', views.engineer_active_ticket, name='engineer-active-ticket'),
    path('engineer-resolved-ticket/', views.engineer_resolved_ticket, name='engineer-resolved-ticket'),
    path('assign-ticket/<str:ticket_id>', views.assign_ticket, name='assign-ticket'),
    path('details-ticket/<str:ticket_id>', views.ticket_detail, name='details-ticket'),
    path('queue-ticket/', views.ticket_queue, name='queue-ticket'),
    path('resolve-ticket<str:ticket_id>/', views.resolve_ticket, name='resolve-ticket'),

]
