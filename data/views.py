import datetime

from django.views.generic import ListView

from data.models import Report


# Create your views here.
class DataListView(ListView):
    model = Report
    paginate_by = 25

    def get_queryset(self):
        if Report.objects.filter(createdDay__gte=datetime.date.today() - datetime.timedelta(days=1)).count() == 0:
            return Report.objects.filter(createdDay__gte=datetime.date.today() - datetime.timedelta(days=2))
        else:
            return Report.objects.filter(createdDay__gte=datetime.date.today() - datetime.timedelta(days=1))
