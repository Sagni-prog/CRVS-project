from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib import messages
from django.core.files.storage import FileSystemStorage #To upload Profile Picture
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
from django.contrib.auth.decorators import login_required
import json

# import os
# from django.conf import settings
# from django.http import HttpResponse
# from django.template.loader import get_template
# from xhtml2pdf import pisa
# from django.contrib.staticfiles import finders


#              # import python module

# # Define your data
# source_html = "<html><body><p>To PDF or not to PDF</p></body></html>"
# output_filename = "test.pdf"

# # Utility function
# def convert_html_to_pdf(source_html, output_filename):
#     # open output file for writing (truncated binary)
#     result_file = open(output_filename, "w+b")

#     # convert HTML to PDF
#     pisa_status = pisa.CreatePDF(
#             source_html,                # the HTML to convert
#             dest=result_file)           # file handle to recieve result

#     # close output file
#     result_file.close()                 # close output file

#     # return False on success and True on errors
#     return pisa_status.err

# # Main program
# if __name__ == "__main__":
#     pisa.showLogging()
#     convert_html_to_pdf(source_html, output_filename)

# def link_callback(uri, rel):
#             """
#             Convert HTML URIs to absolute system paths so xhtml2pdf can access those
#             resources
#             """
#             result = finders.find(uri)
#             if result:
#                     if not isinstance(result, (list, tuple)):
#                             result = [result]
#                     result = list(os.path.realpath(path) for path in result)
#                     path=result[0]
#             else:
#                     sUrl = settings.STATIC_URL        # Typically /static/
#                     sRoot = settings.STATIC_ROOT      # Typically /home/userX/project_static/
#                     mUrl = settings.MEDIA_URL         # Typically /media/
#                     mRoot = settings.MEDIA_ROOT       # Typically /home/userX/project_static/media/

#                     if uri.startswith(mUrl):
#                             path = os.path.join(mRoot, uri.replace(mUrl, ""))
#                     elif uri.startswith(sUrl):
#                             path = os.path.join(sRoot, uri.replace(sUrl, ""))
#                     else:
#                             return uri

#             # make sure that file exists
#             if not os.path.isfile(path):
#                     raise Exception(
#                             'media URI must start with %s or %s' % (sUrl, mUrl)
#                     )
#             return path


# def render_pdf_view(request):
#     template_path = 'user_printer.html'
#     context = {'myvar': 'this is your template context'}
#     # Create a Django response object, and specify content_type as pdf
#     response = HttpResponse(content_type='application/pdf')
#     response['Content-Disposition'] = 'attachment; filename="report.pdf"'
#     # find the template and render it.
#     template = get_template(template_path)
#     html = template.render(context)

#     # create a pdf
#     pisa_status = pisa.CreatePDF(
#        html, dest=response, link_callback=link_callback)
#     # if error then show some funny view
#     if pisa_status.err:
#        return HttpResponse('We had some errors <pre>' + html + '</pre>')
#     return response

@login_required(login_url='login')
def kebeleemployee_home(request):
    # Fetching All Students under Staff
    return render(request, "kebelemployee/employee_home_template.html")


