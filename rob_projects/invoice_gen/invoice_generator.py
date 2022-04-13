from weasyprint import HTML
import flask


html = HTML('invoice.html')
html.write_pdf('invoice.pdf')



