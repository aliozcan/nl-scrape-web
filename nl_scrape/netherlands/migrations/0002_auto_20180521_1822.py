from django.db import migrations
import os
import requests
import zipfile
from django.contrib.gis.utils import LayerMapping
from ..models import province_mapping, region_mapping, country_mapping


def run(apps, schema_editor):
    Country = apps.get_model('netherlands', 'Country')
    Province = apps.get_model('netherlands', 'Province')
    Region = apps.get_model('netherlands', 'Region')

    response = requests.get("http://biogeo.ucdavis.edu/data/diva/adm/NLD_adm.zip")

    data_directory = 'data'
    if not os.path.exists(data_directory):
        os.makedirs(data_directory)

    data_path = os.path.join(os.path.dirname(__file__), os.pardir, 'data')

    with open(os.path.join(data_path, 'NLD_adm.zip'), 'wb+') as f:
        f.write(response.content)

    with zipfile.ZipFile(os.path.join(data_path, 'NLD_adm.zip'), 'r') as zip_ref:
        zip_ref.extractall(os.path.join(data_path, os.pardir, 'data'))

    country_shp = os.path.abspath(
        os.path.join(os.path.dirname(__file__), os.pardir, 'data', 'NLD_adm0.shp'),
    )

    province_shp = os.path.abspath(
        os.path.join(os.path.dirname(__file__), os.pardir, 'data', 'NLD_adm1.shp'),
    )

    region_shp = os.path.abspath(
        os.path.join(os.path.dirname(__file__),  os.pardir, 'data', 'NLD_adm2.shp'),
    )
    ct = LayerMapping(
        Country, country_shp, country_mapping,
        transform=False, encoding='iso-8859-1',
    )
    ct.save(strict=True, verbose=True)

    pr = LayerMapping(
        Province, province_shp, province_mapping,
        transform=False, encoding='iso-8859-1',
    )
    pr.save(strict=True, verbose=True)


    rg = LayerMapping(
        Region, region_shp, region_mapping,
        transform=False, encoding='iso-8859-1',
    )
    rg.save(strict=True, verbose=True)



class Migration(migrations.Migration):
    dependencies = [
        ('scrape', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(run),
    ]