from django.core.management.base import BaseCommand
from octofit_tracker.models import User, Team, Workout, Activity, Leaderboard
from django.utils import timezone

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **kwargs):
        # Clear existing data
        Activity.objects.all().delete()
        Leaderboard.objects.all().delete()
        User.objects.all().delete()
        Team.objects.all().delete()
        Workout.objects.all().delete()

        # Create teams
        marvel = Team.objects.create(name='Marvel')
        dc = Team.objects.create(name='DC')

        # Create users
        users = [
            User.objects.create(name='Spider-Man', email='spiderman@marvel.com', team=marvel),
            User.objects.create(name='Iron Man', email='ironman@marvel.com', team=marvel),
            User.objects.create(name='Wonder Woman', email='wonderwoman@dc.com', team=dc),
            User.objects.create(name='Batman', email='batman@dc.com', team=dc),
        ]

        # Create workouts
        run = Workout.objects.create(name='Running', description='Run fast!')
        lift = Workout.objects.create(name='Weight Lifting', description='Lift heavy!')
        swim = Workout.objects.create(name='Swimming', description='Swim like a fish!')

        # Create activities
        Activity.objects.create(user=users[0], workout=run, date=timezone.now().date(), duration=30, points=10)
        Activity.objects.create(user=users[1], workout=lift, date=timezone.now().date(), duration=45, points=15)
        Activity.objects.create(user=users[2], workout=swim, date=timezone.now().date(), duration=60, points=20)
        Activity.objects.create(user=users[3], workout=run, date=timezone.now().date(), duration=25, points=8)

        # Create leaderboard
        for user in users:
            total_points = sum(a.points for a in user.activities.all())
            Leaderboard.objects.create(user=user, total_points=total_points)

        self.stdout.write(self.style.SUCCESS('octofit_db database populated with test data.'))
