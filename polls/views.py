from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Poll, Choice, Vote
from .forms import PollAddForm, PollEditForm, ChoiceAddForm
# Create your views here.


def check_admin(user):
    return user.is_superuser


class PollsList(LoginRequiredMixin, ListView):
    model = Poll
    template_name = 'polls/polls_list.html'
    context_object_name = 'polls'


@login_required
def PollsDetail(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    if not poll.active:
        context = {
            'poll': poll
        }
        return render(request, 'polls/polls_result.html', context)
    context = {
        'poll': poll
    }
    return render(request, 'polls/polls_detail.html', context)


@login_required
def PollsVote(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    choice_pk = request.POST.get('choice')
    if not poll.user_can_vote(request.user):
        messages.error(request, 'You already voted this poll', extra_tags='alert alert-warning alert-dismissible fade show')
        return redirect('polls:list')
    if choice_pk:
        choice = Choice.objects.get(pk=choice_pk)
        vote = Vote(user=request.user, poll=poll, choice=choice)
        vote.save()
        print(vote)
    else:
        messages.error(request, 'No choice selected', extra_tags='alert alert-warning alert-dismissible fade show')
        return redirect('polls:detail', poll.pk)
    context = {
        'poll': poll
    }
    return render(request, 'polls/polls_result.html', context)


@user_passes_test(check_admin)
def PollsAdd(request):
    if request.method == 'POST':
        form = PollAddForm(request.POST)
        if form.is_valid():
            poll = form.save(commit=False)
            poll.owner = request.user
            poll.save()
            new_choice1 = Choice(poll=poll, choice_text=form.cleaned_data['choice1']).save()
            new_choice2 = Choice(poll=poll, choice_text=form.cleaned_data['choice2']).save()
            new_choice3 = Choice(poll=poll, choice_text=form.cleaned_data['choice3']).save()
            messages.success(request, 'Poll and choices added successfully', extra_tags='alert alert-success alert-dismissible fade show')
            return redirect('polls:list')
    else:
        form = PollAddForm()
    context = {
        'form': form
    }
    return render(request, 'polls/polls_add.html', context)


@user_passes_test(check_admin)
def PollsEdit(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    if request.method == 'POST':
        form = PollEditForm(request.POST, instance=poll)
        if form.is_valid():
            form.save()
            messages.success(request, 'Poll updated successfully', extra_tags='alert alert-warning alert-dismissible fade show')
            return redirect('polls:list')
    else:
        form = PollEditForm(instance=poll)
    context = {
        'form': form,
        'poll': poll
    }
    return render(request, 'polls/polls_edit.html', context)


@user_passes_test(check_admin)
def PollsDelete(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    poll.delete()
    messages.success(request, 'Poll deleted successfully', extra_tags='alert alert-warning alert-dismissible fade show')
    return redirect('polls:list')


@user_passes_test(check_admin)
def ChoiceAdd(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    if request.method == 'POST':
        form = ChoiceAddForm(request.POST)
        new_choice = form.save(commit=False)
        new_choice.poll = poll
        new_choice.save()
        messages.success(request, 'Choice added successfully', extra_tags='alert alert-warning alert-dismissible fade show')
        return redirect('polls:detail', poll.pk)
    else:
        form = ChoiceAddForm()
    context = {
        'form': form
    }
    return render(request, 'polls/choice_add.html', context)


@user_passes_test(check_admin)
def ChoiceEdit(request, choice_id):
    choice = get_object_or_404(Choice, pk=choice_id)
    poll = get_object_or_404(Poll, pk=choice.poll.pk)
    if request.method == 'POST':
        form = ChoiceAddForm(request.POST, instance=choice)
        new_choice = form.save(commit=False)
        new_choice.poll = poll
        new_choice.save()
        messages.success(request, 'Choice updated successfully', extra_tags='alert alert-warning alert-dismissible fade show')
        return redirect('polls:edit', poll.pk)
    else:
        form = ChoiceAddForm(instance=choice)
    context = {
        'form': form,
        'edit_choice': True,
        'choice': choice
    }
    return render(request, 'polls/choice_add.html', context)


@user_passes_test(check_admin)
def ChoiceDelete(request, choice_id):
    choice = get_object_or_404(Choice, pk=choice_id)
    poll = get_object_or_404(Poll, pk=choice.poll.pk)
    choice.delete()
    messages.success(request, 'Choice deleted successfully', extra_tags='alert alert-warning alert-dismissible fade show')
    return redirect('polls:edit', poll.pk)


@user_passes_test(check_admin)
def EndPoll(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    if poll.active is True:
        poll.active = False
        poll.save()
        context = {
            'poll': poll
        }
        return render(request, 'polls/polls_result.html', context)
    else:
        context = {
            'poll': poll
        }
        return render(request, 'polls/polls_result.html', context)















