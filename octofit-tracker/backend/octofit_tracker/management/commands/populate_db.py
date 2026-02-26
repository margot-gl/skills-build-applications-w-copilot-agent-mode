from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from djongo import models

from django.db import connection

from octofit_tracker import settings

from django.apps import apps

class Team(models.Model):
    name = models.CharField(max_length=100, unique=True)
    class Meta:
        app_label = 'octofit_tracker'

class Activity(models.Model):
    user = models.CharField(max_length=100)
    type = models.CharField(max_length=100)
    duration = models.IntegerField()
    class Meta:
        app_label = 'octofit_tracker'

class Leaderboard(models.Model):
    user = models.CharField(max_length=100)
    team = models.CharField(max_length=100)
    score = models.IntegerField()
    class Meta:
        app_label = 'octofit_tracker'

class Workout(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    class Meta:
        app_label = 'octofit_tracker'

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        User = get_user_model()
        # Delete all data
        User.objects.all().delete()
        Team.objects.all().delete()
        Activity.objects.all().delete()
        Leaderboard.objects.all().delete()
        Workout.objects.all().delete()

        # Create teams
        marvel = Team.objects.create(name='Marvel')
        dc = Team.objects.create(name='DC')

        # Create users
        users = [
            User.objects.create_user(username='ironman', email='ironman@marvel.com', password='password', first_name='Tony', last_name='Stark'),
            User.objects.create_user(username='spiderman', email='spiderman@marvel.com', password='password', first_name='Peter', last_name='Parker'),
            User.objects.create_user(username='batman', email='batman@dc.com', password='password', first_name='Bruce', last_name='Wayne'),
            User.objects.create_user(username='wonderwoman', email='wonderwoman@dc.com', password='password', first_name='Diana', last_name='Prince'),
        ]

        # Create activities
        Activity.objects.create(user='ironman', type='Running', duration=30)
        Activity.objects.create(user='spiderman', type='Cycling', duration=45)
        Activity.objects.create(user='batman', type='Swimming', duration=60)
        Activity.objects.create(user='wonderwoman', type='Yoga', duration=50)

        # Create leaderboard
        Leaderboard.objects.create(user='ironman', team='Marvel', score=100)
        Leaderboard.objects.create(user='spiderman', team='Marvel', score=90)
        Leaderboard.objects.create(user='batman', team='DC', score=95)
        Leaderboard.objects.create(user='wonderwoman', team='DC', score=98)

        # Create workouts
        Workout.objects.create(name='Super Strength', description='Strength training for superheroes')
        Workout.objects.create(name='Agility Boost', description='Agility and flexibility workout')
        Workout.objects.create(name='Endurance Run', description='Long distance running for stamina')

        self.stdout.write(self.style.SUCCESS('octofit_db database populated with test data.'))
