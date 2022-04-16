from flask import Flask, render_template, send_file, request
from weasyprint import HTML
import os
import io
from datetime import datetime

app = Flask(__name__)

# @app.route('/', methods=['GET'])
# def hello_browser():
#     print('Hello browser')
#     try:
#         print(request.get_json())
#     except Exception as ex:
#         print(ex)
#     return 'Hello Browser'

@app.route('/', methods=['GET', 'POST'])
# @app.route('/')
def hello_world():
    today = datetime.today().strftime("%B %d, %Y")
    posted_data = request.get_json() or {}
    # invoice_number = 123
    default_data = {
        'duedate': 'August 1, 2019',
        'from_addr': {
            'addr1': '12345 Sunny Road',
            'addr2': 'Sunnyville, CA 12345',
            'company_name': 'Python Tip'
        },
        'invoice_number': 321,
        'items': [{
                'charge': 300.0,
                'title': 'website design'
            },
            {
                'charge': 75.0,
                'title': 'Hosting (3 months)'
            },
            {
                'charge': 10.0,
                'title': 'Domain name (1 year)'
            }
        ],
        'to_addr': {
            'company_name': 'Acme Corp',
            'person_email': 'john@example.com',
            'person_name': 'John Dilly'
        }
    }
    from_addr = {
        'company_name': 'Python Tip',
        'addr1': '12345 Sunny Road',
        'addr2': 'Chicago, Il, USA 60606'
    }
    to_addr = {
        'company_name': 'Acme Corp',
        'person_name': 'Rob Weddell',
        'person_email': 'rweddell@example.com'
    }
    items = [
        {
            'title': 'website design',
            'charge': 300.00
        },{
            'title': 'Hosting (3 months)',
            'charge': 75.00
        },{
            'title': 'Domain name (1 year)',
            'charge': 10.00
        }
    ]
    # duedate = posted_data.get('duedate', default_data['duedate'])
    # from_addr = posted_data.get('from_addr', default_data['from_addr'])
    # to_addr = posted_data.get('to_addr', default_data['to_addr'])
    # invoice_number = posted_data.get('invoice_number', default_data['invoice_number'])
    # items = posted_data.get('items', default_data['items'])
    # total = sum([i['charge'] for i in items])
    # rendered = render_template('invoice.html',
    #                         date = today,
    #                         from_addr = from_addr,
    #                         to_addr = to_addr,
    #                         items = items,
    #                         total = total,
    #                         invoice_number = invoice_number,
    #                         duedate = duedate)
    duedate = posted_data.get('duedate', default_data['duedate'])
    from_addr = posted_data.get('from_addr', default_data['from_addr'])
    to_addr = posted_data.get('to_addr', default_data['to_addr'])
    invoice_number = posted_data.get('invoice_number', default_data['invoice_number'])
    items = posted_data.get('items', default_data['items'])
    total = sum([i['charge'] for i in items])
    rendered = render_template('invoice.html',
                            date = today,
                            from_addr = posted_data.get('from_addr', default_data['from_addr']),
                            to_addr = posted_data.get('to_addr', default_data['to_addr']),
                            items = posted_data.get('items', default_data['items']),
                            total = sum([i['charge'] for i in items]),
                            invoice_number = posted_data.get('invoice_number', default_data['invoice_number']),
                            duedate = posted_data.get('duedate', default_data['duedate']))
    html = HTML(string=rendered)
    rendered_pdf = html.write_pdf() #'invoice.pdf')
    return send_file(
            io.BytesIO(rendered_pdf),
            attachment_filename='invoice.pdf'
        )



if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)