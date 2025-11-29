from django.shortcuts import render

def scan_view(request):
    return render(request, "scanner/scan.html")
