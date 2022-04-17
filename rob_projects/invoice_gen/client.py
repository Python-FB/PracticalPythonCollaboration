import requests
import json

url = 'http://127.0.0.1:5000/'
data = {
    'duedate': 'September 1, 2022',
    'from_addr': {
        'addr1': 'Chicago, Illinois',
        'addr2': 'Sunnyville, CA 12345',
        'company_name': 'Python_FB'
    },
    'invoice_number': '156',
    'items': [{
            'charge': 500.0,
            'title': 'Brochure design'
        },
        {
            'charge': 85.0,
            'title': 'Hosting (6 months)'
        },
        {
            'charge': 10.0,
            'title': 'Domain name (1 year)'
        }
    ],
    'to_addr': {
        'company_name': 'The Cave',
        'person_email': 'rweddell@example.com',
        'person_name': 'Rob Weddell'
    }
}

user_response = ''

while user_response != 'no':
    data['duedate'] = input('new date : ')
    print('new_due_date', data['duedate'])
    file_name = input('new file name?: ')
    user_response = input('continue?: ')
    html = requests.post(url, json=data)

    with open(f'{file_name}.pdf', 'wb') as f:
        f.write(html.content)