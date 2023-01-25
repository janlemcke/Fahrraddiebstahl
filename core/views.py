import datetime

from django.views.generic.base import TemplateView

from data.models import Report


class MainView(TemplateView):
    template_name = "core/main.html"

    def get_context_data(self, **kwargs):
        context = {}
        context["total_count"] = Report.objects.all().count()

        newest_data_count = Report.objects.filter(createdDay__gte=datetime.date.today() - datetime.timedelta(days=1)).count()
        context["newest_data_date"] = "Gestern"
        if newest_data_count == 0:
            newest_data_count = Report.objects.filter(createdDay__gte=datetime.date.today() - datetime.timedelta(days=2)).count()
            context["newest_data_date"] = "Vorgestern"
        context["newest_data_count"] = newest_data_count
        return context
