import datetime
from io import BytesIO
from urllib import response
from django.http import HttpResponse
from django.template.loader import get_template

from xhtml2pdf import pisa

from payment.models import Transaction

def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None

from django.http import HttpResponse
from django.views.generic import View

 

class GeneratePdf(View):
    def get(self, request, *args, **kwargs):
        tran = Transaction.objects.filter(user=request.user).order_by('-tran_date').first()
        text_item = tran.items
        items = text_item.split('.')
        
        data = {
             'today': datetime.date.today(), 
             'amount': tran.amount,
            'customer_name': tran.name,
            'order_id': tran.tran_id,
            'items': items,
            'total': tran.amount,
        }
        pdf = render_to_pdf('pdf/invoice.html', data)
        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            filename = "Invoice_%s.pdf" %("12341231")
            content = "inline; filename='%s'" %(filename)
            download = request.GET.get("download") or True
            if download:
                content = "attachment; filename='%s'" %(filename)
                response['Content-Disposition'] = content
                return response
            return HttpResponse("Not found")