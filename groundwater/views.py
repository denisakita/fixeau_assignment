import csv
import os
import re

from django.conf import settings
from django.core.paginator import PageNotAnInteger, Paginator, EmptyPage
from django.http import HttpResponse
from django.shortcuts import render

from groundwater.forms import GroundLevelForm
from models.models import GroundWater

"""  Create an API call that can
 1. Read in the three csv’s attached in the mail and combines them
 2. Remove outliers from the combined data
 3. Insert the data into a table  """


def upload_csv(request):
    if request.method == "POST" and request.FILES.get("csv_file"):
        uploaded_file = request.FILES["csv_file"]

        # Create the directory if it isn`t to save tha Cvs that we have to upload
        media_dir = os.path.join(settings.MEDIA_ROOT, "uploaded_csvs")
        os.makedirs(media_dir, exist_ok=True)
        file_path = os.path.join(media_dir, uploaded_file.name)

        #  Open file to write dhe data that we uploaded
        with open(file_path, "wb") as destination:
            for chunk in uploaded_file.chunks():
                destination.write(chunk)

        combined_data = []
        # Open CSV to read
        with open(file_path, "r", encoding='utf-8') as csvfile:
            csvreader = csv.reader(csvfile)
            next(csvreader)
            next(csvreader)
            for row in csvreader:
                if len(row) >= 2:
                    date, measurement = row
                elif len(row) == 1:
                    date = row[0]
                    measurement = 0
                else:
                    print(f"Row with no data: {row}")
                    continue
                #  Extract a valid date format because some data has problems
                match = re.match(r"(\d{4}-\d{2}-\d{2})", date)
                if match:
                    date = match.group(1)
                else:
                    print(f"Invalid date format: {date}")
                    continue

                combined_data.append({
                    'date': date,
                    'measurement': measurement
                })

        # Insert the data into the database for GroundWaterModel
        for data in combined_data:
            GroundWater.objects.create(**data)
        # Success Response
        return HttpResponse("Data imported successfully")

    return render(request, 'upload_csv.html')


""" Create an API call that:
1. Returns the data from the table
2. Contains a ground level query parameter that returns the data relative to this ground level"""


def list_groundwater(request):
    # Get the 'ground_level' query param based on the request
    ground_level = request.GET.get('ground_level', 0)
    data = GroundWater.objects.filter(measurement__gte=ground_level)

    # Paginator to paginate data to look better  with 10 items per page
    paginator = Paginator(data, 10)
    page = request.GET.get('page')

    try:
        data = paginator.page(page)
    except PageNotAnInteger:
        data = paginator.page(1)
    except EmptyPage:
        data = paginator.page(paginator.num_pages)

    form = GroundLevelForm()
    # Render the 'template.html' and pass data to display
    return render(request, 'template.html', {'data': data, 'form': form})


def show_form(request):
    form = GroundLevelForm()
    return render(request, 'template.html', {'form': form})
