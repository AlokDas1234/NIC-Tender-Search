from django.shortcuts import render

# Create your views here.

import pandas as pd
from django.db import connection
from django.shortcuts import render
from django.http import HttpResponse
from .models import Client, TenderResults


def index(request):
    if request.method == "POST":
        uploaded_file = request.FILES.get("file")
        filename = uploaded_file.name.lower()

        # Read Excel
        if filename.endswith(".xlsx") or filename.endswith(".xls"):
            df = pd.read_excel(uploaded_file)

        # Read CSV with safe encoding
        else:
            df = pd.read_csv(uploaded_file, encoding="latin1")

        objs = [
            Client(
                state_name=row["state_name"],
                site_url=row["site_url"],
                search_key=row["search_key"],
                exclude_key=row["exclude_key"]
            )
            for _, row in df.iterrows()
        ]

        # ---- FIX SQLITE BUG HERE ----
        if connection.connection is None:
            connection.connect()
        # -------------------------------

        Client.objects.bulk_create(objs)
        return HttpResponse("Form submitted successfully!")
    return render(request, "home/index.html")

def show_data(request):
    clients = Client.objects.all()
    return render(request, "home/show_data.html", {"clients": clients})


from .tasks import run_scraper
def run_task(request):
    run_scraper.delay()
    return HttpResponse("Scraper started!")

def show_tender_data(request):
    results = TenderResults.objects.all()
    return render(request, "home/tender_result.html", {"results": results})
