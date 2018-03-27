from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from imageXback.models import Member

class Command(BaseCommand):
    def handle(self, *args, **options):
        User.objects.all().delete()
        Member.objects.all().delete()