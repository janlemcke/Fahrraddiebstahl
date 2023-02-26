import calendar

from django.db.models import Sum
from django.db.models.functions import ExtractIsoWeekDay
from django.utils import timezone
from ninja import NinjaAPI
from ninja.responses import Response

from data.models import Report

api = NinjaAPI(csrf=True)

VALID_COMPARISON_TYPES = ["day", "week", "month", "year"]
COMPARISON_TYPE_MAP = {
    "day": ("yesterday", "day_before"),
    "week": ("this_week", "last_week"),
    "month": ("this_month", "last_month"),
    "year": ("this_year", "last_year"),
}

COMPARISON_TYPE_LABEL_MAP = {
    "day": ("Aktueller Tag", "Gestern"),
    "week": ("Aktuelle Woche", "Letze Woche"),
    "month": ("Aktueller Monat", "Letzter Monat"),
    "year": ("Aktuelles Jahr", "Letztes Jahr"),
}


def get_comparison_date_range(comparison_type):
    now = timezone.now()
    if comparison_type == "yesterday":
        # TODO get latest day for which we have data.
        start_date = now - timezone.timedelta(days=1)
        end_date = now
    elif comparison_type == "last_month":
        start_date = now - timezone.timedelta(days=now.day)
        end_date = start_date + timezone.timedelta(days=calendar.monthrange(now.year, now.month - 1)[1])
    elif comparison_type == "this_month":
        start_date = now - timezone.timedelta(days=now.day - 1)
        end_date = start_date + timezone.timedelta(days=calendar.monthrange(now.year, now.month)[1] - 1)
    elif comparison_type == "last_week":
        start_date = now - timezone.timedelta(days=now.weekday() + 7)
        end_date = start_date + timezone.timedelta(days=6)
    elif comparison_type == "this_week":
        start_date = now - timezone.timedelta(days=now.weekday())
        end_date = start_date + timezone.timedelta(days=6)
    elif comparison_type == "last_year":
        start_date = now - timezone.timedelta(days=now.timetuple().tm_yday + 365)
        end_date = now - timezone.timedelta(days=now.timetuple().tm_yday + 1)
    elif comparison_type == "this_year":
        start_date = now - timezone.timedelta(days=now.timetuple().tm_yday - 1)
        end_date = now
    else:
        start_date = None
        end_date = None

    return start_date, end_date


@api.get("/damageComparison/{comparison_type}")
def get_damage_comparison(request, comparison_type) -> Response:
    current_comparison_type, last_comparison_type = COMPARISON_TYPE_MAP.get(comparison_type, (None, None))
    if not current_comparison_type or not last_comparison_type:
        return Response({"error": "Invalid comparison type parameter"}, status=400)

    current_start, current_end = get_comparison_date_range(current_comparison_type)
    last_start, last_end = get_comparison_date_range(last_comparison_type)

    # Query for current week
    current_data = Report.objects.filter(
        createdDay__range=(current_start, current_end)
    ).annotate(
        # Return Monday=1 through Sunday=7, based on ISO-8601.
        week_day=ExtractIsoWeekDay('createdDay')
    ).values('week_day').annotate(
        damage_sum=Sum('damageValue')
    )

    # Query for last week
    last_data = Report.objects.filter(
        createdDay__range=(last_start, last_end)
    ).annotate(
        week_day=ExtractIsoWeekDay('createdDay')
    ).values('week_day').annotate(
        damage_sum=Sum('damageValue')
    )

    current_data = list(map(lambda x: x["damage_sum"], current_data))
    last_data = list(map(lambda x: x["damage_sum"], last_data))
    return Response({"current_data": current_data,
                     "last_data": last_data,
                     "labels": COMPARISON_TYPE_LABEL_MAP[comparison_type]})


def divide_damagevalue_per_hour(raw_data):
    """
        Divides the damage value in raw_data by the number of hours in the range
        and returns the average damage value per hour for each hour in a day.
    """
    converted_dataset = [hour for hour in range(24)]
    print(converted_dataset)
    for data in raw_data:
        day_difference = (data["endDay"] - data["beginDay"]).days
        amount_of_hours = day_difference * 24 + (data['endHour'] - data['beginHour'])
        if amount_of_hours != 0:
            avg = data["damageValue"] / amount_of_hours
        else:
            avg = data["damageValue"]

        hours = [(data['beginHour'] + i) % 24 for i in range(amount_of_hours)]
        for hour in hours:
            converted_dataset[hour] += avg
    return list(map(lambda x: round(x, 2), converted_dataset))


@api.get("/damageValuePerHour/{comparison_type}")
def get_damagevalue_per_hours(request, comparison_type: str) -> Response:
    current_comparison_type, last_comparison_type = COMPARISON_TYPE_MAP.get(comparison_type, (None, None))
    if not current_comparison_type or not last_comparison_type:
        return Response({"error": "Invalid comparison type parameter"}, status=400)

    current_start, current_end = get_comparison_date_range(current_comparison_type)
    last_start, last_end = get_comparison_date_range(last_comparison_type)

    current_data = Report.objects.filter(createdDay__range=(current_start, current_end)).values(
        'beginHour', 'endHour',
        'beginDay', 'endDay',
        'damageValue')
    last_data = Report.objects.filter(createdDay__range=(last_start, last_end)).values(
        'beginHour', 'endHour',
        'beginDay', 'endDay',
        'damageValue')

    return Response({"current_data": divide_damagevalue_per_hour(current_data),
                     "last_data": divide_damagevalue_per_hour(last_data),
                     "labels": COMPARISON_TYPE_LABEL_MAP[comparison_type]
                     })
