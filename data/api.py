import datetime
from typing import List

from django.db.models import Sum
from django.db.models.functions import TruncDay, ExtractWeekDay, ExtractIsoWeekDay
from django.utils import timezone
from ninja import NinjaAPI, Schema

from data.models import Report

api = NinjaAPI(csrf=True)


def get_current_last_week_start_ends():
    # Get the current week
    now = timezone.now()
    current_week_start = now - timezone.timedelta(days=now.weekday())
    current_week_end = current_week_start + timezone.timedelta(days=6)

    # Get the last week
    last_week_start = current_week_start - timezone.timedelta(days=7)
    last_week_end = last_week_start + timezone.timedelta(days=6)

    return current_week_start, current_week_end, last_week_start, last_week_end


@api.get("/damageComparison")
def get_damage_comparison(request):
    current_week_start, current_week_end, last_week_start, last_week_end = get_current_last_week_start_ends()

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


def divide_damagevalue_per_hour(raw_data):
    convertedDataset = [0] * 24
    for i in raw_data:
        dayDifference = abs((i["beginDay"] - i["endDay"]).days)
        if dayDifference > 1:
            tmpDays = [0] * dayDifference * 24
            amountOfHours = (i['endHour'] - i['beginHour']) % 24
            amountOfHours += (dayDifference - 1) * 24
            if amountOfHours != 0:
                avg = round(i["damageValue"] / amountOfHours, 2)
            else:
                avg = i["damage"]

            for j in range(i["beginHour"], i["beginHour"] + amountOfHours):
                tmpDays[j % (24 * dayDifference)] += avg

            for k in range(0, len(tmpDays)):
                convertedDataset[k % 24] += tmpDays[k]
        else:
            j = (i['endHour'] - i['beginHour']) % 24
            if j != 0:
                avg = round(i["damageValue"] / j, 2)
            else:
                avg = i["damageValue"]
            for tmp in range(i['beginHour'], i['beginHour'] + j):
                convertedDataset[tmp % 24] += avg
    return list(map(lambda x: round(x,2), convertedDataset))


@api.get("/damageValuePerHour")
def get_damagevalue_per_hours(request):
    current_week_start, current_week_end, last_week_start, last_week_end = get_current_last_week_start_ends()
    current_week_data = Report.objects.filter(createdDay__range=(current_week_start, current_week_end)).values(
        'beginHour', 'endHour',
        'beginDay', 'endDay',
        'damageValue')
    last_week_data = Report.objects.filter(createdDay__range=(last_week_start, last_week_end)).values(
        'beginHour', 'endHour',
        'beginDay', 'endDay',
        'damageValue')

    return {"current_week_data": divide_damagevalue_per_hour(current_week_data),
            "last_week_data": divide_damagevalue_per_hour(last_week_data)}
