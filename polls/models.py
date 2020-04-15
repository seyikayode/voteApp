from django.db import models
from django.contrib.auth.models import User
import secrets
# Create your models here.

class Poll(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    def __str__(self):
        return self.text
    def user_can_vote(self, user):
        user_votes = user.vote_set.all()
        qs = user_votes.filter(poll=self)
        if qs.exists():
            return False
        else:
            return True
    @property
    def get_vote_count(self):
        return self.vote_set.count()
    def get_result_dict(self):
        result = []
        for choice in self.choice_set.all():
            d = {}
            alert_class = ['primary', 'secondary', 'success', 'danger', 'dark', 'warning', 'info']
            d['alert_class'] = secrets.choice(alert_class)
            d['text'] = choice.choice_text
            d['num_votes'] = choice.get_vote_count
            if not self.get_vote_count:
                d['percentage'] = 0
            else:
                d['percentage'] = (choice.get_vote_count / self.get_vote_count)*100
            result.append(d)
        return result

class Choice(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=255)
    def __str__(self):
        return f'{self.poll.text[:25]} - {self.choice_text[:25]}'
    @property
    def get_vote_count(self):
        return self.vote_set.count()

class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
    def __str__(self):
        return f'{self.poll.text[:15]} - {self.choice.choice_text[:15]} - {self.user.username}'
