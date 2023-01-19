import hashlib
from django.core.management.base import BaseCommand
import pandas as pd

from data.models import Report


class Command(BaseCommand):
    help = 'Loads bike theft data from berlin police.'

    def handle(self, *args, **kwargs):
        url = "https://www.internetwache-polizei-berlin.de/vdb/Fahrraddiebstahl.csv"
        csv = pd.read_csv(url, encoding='unicode_escape')

        convert_to_us_date = lambda x: x[-4:] + "-" + x[-7:-5] + "-" + x[:2]

        csv["ANGELEGT_AM"] = csv["ANGELEGT_AM"].apply(convert_to_us_date)
        csv["TATZEIT_ANFANG_DATUM"] = csv["TATZEIT_ANFANG_DATUM"].apply(convert_to_us_date)
        csv["TATZEIT_ENDE_DATUM"] = csv["TATZEIT_ENDE_DATUM"].apply(convert_to_us_date)

        for i, row in csv.iterrows():
            lor = str(row["LOR"])
            if len(lor) < 8:
                lor = lor.zfill(8)

            tmp = str(row["ANGELEGT_AM"]) + str(row["TATZEIT_ANFANG_DATUM"]) + str(row["TATZEIT_ANFANG_STUNDE"]) + str(
                row["TATZEIT_ENDE_DATUM"]) + str(row["TATZEIT_ENDE_STUNDE"]) + lor + str(row["ART_DES_FAHRRADS"]) + str(
                row["DELIKT"])
            hash = hashlib.md5(tmp.encode()).hexdigest()

            if Report.objects.filter(pk=hash).exists():
                continue
            else:
                report = Report.create(row["ANGELEGT_AM"], row["TATZEIT_ANFANG_DATUM"], row["TATZEIT_ANFANG_STUNDE"],
                                row["TATZEIT_ENDE_DATUM"], row["TATZEIT_ENDE_STUNDE"], lor, row["SCHADENSHOEHE"],
                                row["VERSUCH"], row["ART_DES_FAHRRADS"], row["DELIKT"], row["ERFASSUNGSGRUND"], hash)
                report.save()
