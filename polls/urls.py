from django.urls import path
from .views import PollsList, PollsDetail, PollsVote, PollsAdd, PollsEdit, PollsDelete, ChoiceAdd, ChoiceEdit, ChoiceDelete, EndPoll
app_name = 'polls'
urlpatterns = [
    path('', PollsList.as_view(), name='list'),
    path('<int:poll_id>/', PollsDetail, name='detail'),
    path('<int:poll_id>/vote/', PollsVote, name='vote'),
    path('add/', PollsAdd, name='add'),
    path('edit/<int:poll_id>/', PollsEdit, name='edit'),
    path('delete/<int:poll_id>/', PollsDelete, name='delete'),
    path('edit/<int:poll_id>/choice/add/', ChoiceAdd, name='add-choice'),
    path('edit/choice/<int:choice_id>/', ChoiceEdit, name='edit-choice'),
    path('delete/choice/<int:choice_id>/', ChoiceDelete, name='delete-choice'),
    path('<int:poll_id>/end/', EndPoll, name='end')
]

