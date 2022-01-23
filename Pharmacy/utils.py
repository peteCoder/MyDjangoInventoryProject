from django.http import response
from django.utils.crypto import get_random_string
from django.core.files.storage import FileSystemStorage
from weasyprint import HTML, CSS
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.conf import settings
import os


def random_string():
	unique_char = get_random_string(length=15)
	return unique_char


