from django.http import HttpResponse
import os

def serve_validation_file(request):
    file_path = os.path.join(os.path.dirname(__file__), 'pki-validation', '5013459ACD3259D4CE7E743FD5D06B66.txt')
    with open(file_path, 'r') as f:
        validation_content = f.read()
    return HttpResponse(validation_content, content_type="text/plain")
