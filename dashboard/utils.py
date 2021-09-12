from django.template.loader import get_template
from django.http import HttpResponse
from io import BytesIO

from xhtml2pdf import pisa

def pdf_report_create(template, file_name, context={}):
        template = get_template(template)
        html = template.render(context)
        result = BytesIO()
        response = HttpResponse(result.getvalue(), content_type="application/pdf")
        response['Content-Disposition'] = 'attachment; filename={}'.format(file_name)
        pdf = pisa.CreatePDF(html, dest=response)
        if pdf.err:
            return HttpResponse("Errors")
        return response

    
       