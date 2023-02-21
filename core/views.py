import datetime
import json
import os

from django.views.generic.base import TemplateView

from core import settings
from data.models import Report


class MainView(TemplateView):
    template_name = "core/main.html"

    def convert_lor(self, lor):
        with open(os.path.join(settings.BASE_DIR, "core/static/geojson/dictionary.json"), "r") as file:
            data = json.load(file)
            return data[lor]

    def get_context_data(self, **kwargs):
        context = {}
        context["total_count"] = Report.objects.all().count()

        newest_data_count = Report.objects.filter(
            createdDay__gte=datetime.date.today() - datetime.timedelta(days=1)).count()
        context["newest_data_date"] = "Gestern"
        if newest_data_count == 0:
            newest_data_count = Report.objects.filter(
                createdDay__gte=datetime.date.today() - datetime.timedelta(days=2)).count()
            context["newest_data_date"] = "Vorgestern"
        context["newest_data_count"] = newest_data_count

        damageValue_top_five = Report.objects.all().order_by("-damageValue")[:5].values("typeOfBike",
                                                                                        "damageValue",
                                                                                        "beginDay",
                                                                                        "beginHour", "endDay",
                                                                                        "endHour", "lor")
        for object in damageValue_top_five:
            object["lor_small"] = self.convert_lor(object["lor"])
            object["lor_medium"] = self.convert_lor(object["lor"][:6])
            object["lor_large"] = self.convert_lor(object["lor"][:4])

        context["damageValue_top_five"] = damageValue_top_five

        return context
