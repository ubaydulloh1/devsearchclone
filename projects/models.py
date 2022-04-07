from django.db import models
import uuid
from users.models import Profile

# Create your models here.

class Project(models.Model):
    owner = models.ForeignKey(Profile, null=True, blank=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=200, null=True, blank=True)
    featured_img = models.ImageField(blank=True, null=True, default='default.jpg')
    description = models.TextField(null=True, blank=True)
    
    tags = models.ManyToManyField('Tag', blank=True)

    vote_total = models.IntegerField(default=0, null=True, blank=True)
    vote_ratio = models.IntegerField(default=0, null=True, blank=True)
    demo_link = models.CharField(max_length=1000, null=True, blank=True)
    source_link = models.CharField(max_length=1000, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)


    class Meta:
        ordering = ['-vote_ratio', '-vote_total', '-title']

    @property
    def getVote(self):
        vote_total = len(self.review_set.all())
        vote_positive = len(self.review_set.filter(value="up"))
        if vote_total != 0:
            vote_ratio = int((vote_positive / vote_total)*100)
        else:
            vote_ratio = 0
        self.vote_total = vote_total
        self.vote_ratio = vote_ratio
        self.save()        
        return vote_total, vote_ratio

    @property
    def reviewers(self):
        reviewer_s = self.review_set.all().values_list("owner__id", flat=True)
        return reviewer_s

    def __str__(self):
        return self.title


class Review(models.Model):

    VOTE_TYPE = (
        ('up', 'Up Vote'),
        ('down', 'Down Vote'),
    )

    owner = models.ForeignKey(Profile, null=True, blank=True, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    body = models.TextField(null=True, blank=True)
    value = models.CharField(max_length=200, choices=VOTE_TYPE)
    created = models.DateField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    class Meta:
        unique_together = [["owner", "project"]]


    def __str__(self):
        return self.value


class Tag(models.Model):
    name = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return self.name
