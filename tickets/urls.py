from django.urls import path, include
from . import views
from rest_framework_nested import routers
from . import views, api_views

router = routers.DefaultRouter()
router.register(r'tickets', api_views.TicketViewSet, basename='api-ticket')

tickets_router = routers.NestedDefaultRouter(router, r'tickets', lookup='ticket')
tickets_router.register(r'comments', api_views.CommentViewSet, basename='api-ticket-comments')


urlpatterns = [
    path('',                          views.dashboard,      name='dashboard'),
    path('tickets/',                  views.ticket_list,    name='ticket_list'),
    path('tickets/new/',              views.ticket_create,  name='ticket_create'),
    path('tickets/<int:pk>/',         views.ticket_detail,  name='ticket_detail'),
    path('tickets/<int:pk>/edit/',    views.ticket_update,  name='ticket_update'),
    path('tickets/<int:pk>/delete/',  views.ticket_delete,  name='ticket_delete'),
    path('api/', include(router.urls)),
    path('api/', include(tickets_router.urls)),
]