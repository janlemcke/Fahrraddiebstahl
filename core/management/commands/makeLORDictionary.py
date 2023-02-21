import hashlib
import json
import os

from django.core.management.base import BaseCommand
import pandas as pd

from core import settings
from data.models import Report


class Command(BaseCommand):
    help = 'Makes a dictionary and stores it to disk, where the keys are the LOR codes and the values the names.'
    path_to_geojsons = "./core/static/geojson/"
    output_filename = "dictionary.json"

    def handle(self, *args, **kwargs):
        dic = {}
        for name in os.listdir(self.path_to_geojsons):
            if name == self.output_filename:
                continue
            path_to_file = os.path.join(self.path_to_geojsons, name)
            with open(path_to_file, "r") as file:
                json_data = json.load(file)
                for feature in json_data["features"]:
                    key, value = feature["properties"].values()
                    dic[key] = value

        with open(os.path.join(self.path_to_geojsons, self.output_filename), "w") as file:
            json.dump(dic, file)
