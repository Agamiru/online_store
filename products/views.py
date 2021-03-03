from django import forms
from django.shortcuts import render
from django.http.response import HttpResponse
from rest_framework import status

from .utils.admin_utils import CustomHstoreField


class TestForm(forms.Form):
    h_store = CustomHstoreField()


def test_view(request):

    if request.method == "GET":
        return render(request, "test_hstore.html", {"form": TestForm}, status=status.HTTP_200_OK)

    else:
        form = TestForm(request.POST)
        print(request.POST)
        if form.is_valid():
            return HttpResponse("Well done", status=status.HTTP_200_OK)
        return HttpResponse("Bad request", status=status.HTTP_400_BAD_REQUEST)


