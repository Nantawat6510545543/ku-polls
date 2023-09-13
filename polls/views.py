from django.http import HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import Choice, Question, Vote


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        return Question.objects.filter(pub_date__lte=timezone.now()
                                       ).order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())

    def get(self, request, *args, **kwargs):

        try:
            self.object = self.get_object()
        except Http404:
            messages.error(request,
                           "Question does not exist or is not published yet.")
            return redirect("polls:index")

        if not self.object.can_vote():
            return render(request, 'polls/results.html', {
                'question': self.object,
                'message': "Voting has been closed."
            })
        return super().get(request, *args, **kwargs)


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {'latest_question_list': latest_question_list}
    return render(request, 'polls/index.html', context)


def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html',
                  {'question': question})


@login_required
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    user = request.user

    if not user.is_authenticated:
        return redirect('login')

    if not question.can_vote():
        messages.error(request, "Vote is not allow")
        return redirect("polls:index")

    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        messages.error(request, "You didn't select a choice.")
        return HttpResponseRedirect(
            reverse('polls:detail', args=(question.id,)))

    try:
        vote = Vote.objects.get(user=user, choice__question=question)
        vote.choice = selected_choice
    except Vote.DoesNotExist:
        vote = Vote(user=user, choice=selected_choice)

    vote.save()
    return HttpResponseRedirect(
        reverse("polls:results", args=(question.id,)))


def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html',
                  {'question': question})
