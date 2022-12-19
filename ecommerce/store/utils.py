from .models import *


class DataMixin:

    def get_user_context(self, **kwargs):
       cats = Category.objects.all()
       context = kwargs
       context['cats'] = cats
       return context
