# from django.contrib import admin
#
# from moverspackers.models import SiteUser
# from .models import *
#
# # Register your models here.

from django.contrib import admin
from .models import Agent, SiteUser, Services, Contact

admin.site.register(Agent)
admin.site.register(SiteUser)
admin.site.register(Services)
admin.site.register(Contact)

