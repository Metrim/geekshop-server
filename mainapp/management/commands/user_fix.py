from django.core.management import BaseCommand

from authapp.models import User, UserProfile


class Command(BaseCommand):

    def handle(self, *args, **options):
        for user in User.objects.all():
            user_profile = UserProfile.objects.create(user=user)
            user_profile.save()
