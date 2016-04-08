from django.contrib import admin
from vote.models import *

admin.site.register(Vote)
admin.site.register(Poll)
admin.site.register(Choice)
