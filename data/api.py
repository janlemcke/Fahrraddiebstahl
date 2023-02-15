import datetime
from typing import List

from django.db.models import Sum
from django.db.models.functions import TruncDay, ExtractWeekDay, ExtractIsoWeekDay
from django.utils import timezone
from ninja import NinjaAPI, Schema

from data.models import Report

api = NinjaAPI(csrf=True)


@api.get("/damageComparison")
def getDamageComparison(request):
    # Get the current week
    now = timezone.now()
    current_week_start = now - timezone.timedelta(days=now.weekday())
    current_week_end = current_week_start + timezone.timedelta(days=6)

    # Get the last week
    last_week_start = current_week_start - timezone.timedelta(days=7)
    last_week_end = last_week_start + timezone.timedelta(days=6)

    # Query for current week
    current_week_data = Report.objects.filter(
        createdDay__range=(current_week_start, current_week_end)
    ).annotate(
        # Return Monday=1 through Sunday=7, based on ISO-8601.
        week_day=ExtractIsoWeekDay('createdDay')
    ).values('week_day').annotate(
        damage_sum=Sum('damageValue')
    )

    # Query for last week
    last_week_data = Report.objects.filter(
        createdDay__range=(last_week_start, last_week_end)
    ).annotate(
        week_day=ExtractIsoWeekDay('createdDay')
    ).values('week_day').annotate(
        damage_sum=Sum('damageValue')
    )

    current_week_data = list(map(lambda x: x["damage_sum"], current_week_data))
    last_week_data = list(map(lambda x: x["damage_sum"], last_week_data))
    return {"current_week_data": current_week_data, "last_week_data": last_week_data}
