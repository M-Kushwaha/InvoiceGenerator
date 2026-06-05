# importing Flask and other modules
from flask import Flask, request, render_template 
from reportlab.platypus import ( SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle ) 
from reportlab.lib.styles import ( getSampleStyleSheet, ParagraphStyle ) 
from reportlab.lib import colors 
from reportlab.lib.enums import TA_RIGHT 
from reportlab.lib.pagesizes import A4 
from reportlab.lib.units import mm
import mysql.connector as a


mycon = a.connect (host="localhost",user="root", password="*******", database="invoices", ssl_disabled =True )


cursor = mycon.cursor()
app = Flask(__name__)   

# A decorator used to tell the application which URL is associated function
# @app.route('/hello/<name>') - adding name variable to the route
@app.route('/', methods =["GET", "POST"])

def get_invoiceData():
    if request.method == "POST":
       # getting input with name = fname in HTML form
       
       # getting input with name = lname in HTML form 
       date = request.form.get("Date") 
       companyName = request.form.get("company_name")
       companyAddress = request.form.get("company_address") 
       companyEmail = request.form.get("company_email")

       clientName = request.form.get("client_name")
       clientAddress = request.form.get("client_address") 
       clientPhone = request.form.get("client_phone")
       clientEmail = request.form.get("client_email")
       
       productNames = request.form.getlist("product_name[]")
       quantities = request.form.getlist("quantity[]")
       rates = request.form.getlist("rate[]")
       lineTotals = request.form.getlist("line_total[]")

       subTotal = request.form.get("subtotal")
       gstTax = request.form.get("gsttax") 
       grandTotal = request.form.get("grandtotal")
       
       id = save_invoice(date, clientName, clientAddress, clientPhone, clientEmail, subTotal, gstTax, grandTotal)
       save_products(id, productNames, quantities, rates, lineTotals)
       
    return render_template("index.html")

def save_invoice(date, clientName, clientAddress, clientPhone, clientEmail, subTotal, gstTax, grandTotal):
    invoice_query = 'INSERT INTO INVOICE(invoice_date, client_name, client_address, client_phone, client_email, subtotal, gst_percent, grand_total) values(%s,%s, %s, %s, %s, %s, %s, %s)'
    invoice_values = (date, clientName, clientAddress, clientPhone, clientEmail, subTotal, gstTax, grandTotal)
    cursor.execute(invoice_query, invoice_values)
    mycon.commit()
    return cursor.lastrowid


def save_products(id,productNames, quantities, rates, lineTotals):
    for i in range(len(productNames)):
        product_query = 'INSERT INTO PRODUCTS(invoice_id, product_name, quantity, rate, line_total) values(%s,%s, %s,%s, %s)'
        product_values = (id, productNames[i], quantities[i], rates[i], lineTotals[i])
        cursor.execute(product_query, product_values)
    mycon.commit()
    generate_pdf(id)


def get_invoice(id) :
    query = "select * from invoice where invoice_id =%s"
    cursor.execute(query,(id,))
    return cursor.fetchone()


def get_products(id) :
    query = "select * from products where invoice_id =%s"
    cursor.execute(query,(id,))
    return cursor.fetchall()




def generate_pdf(id):

    invoice = get_invoice(id)
    products = get_products(id) # --------------------------------------------------
    # PAGE CONFIGURATION
    # --------------------------------------------------


    pdf = SimpleDocTemplate(
        f"invoices/invoice_{id}.pdf",
        pagesize=A4,
        leftMargin=15 * mm,
        rightMargin=15 * mm,
        topMargin=15 * mm,
        bottomMargin=15 * mm
    )

    story = []

    printable_width = A4[0] - (30 * mm)

    # --------------------------------------------------
    # COLOR PALETTE
    # --------------------------------------------------

    PRIMARY_GREEN = colors.HexColor("#1B3B2B")
    BODY_TEXT = colors.HexColor("#242B27")
    MUTED_TEXT = colors.HexColor("#5A6E63")
    TABLE_TINT = colors.HexColor("#F2F5F3")
    DIVIDER = colors.HexColor("#DCE3DF")

    # --------------------------------------------------
    # STYLES
    # --------------------------------------------------

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "InvoiceTitle",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=24,
        leading=28,
        textColor=colors.HexColor("#111111")
    )

    invoice_meta_style = ParagraphStyle(
        "InvoiceMeta",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=10,
        leading=13,
        textColor=MUTED_TEXT
    )

    company_style = ParagraphStyle(
        "CompanyInfo",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9,
        leading=12,
        alignment=TA_RIGHT,
        textColor=MUTED_TEXT
    )

    company_name_style = ParagraphStyle(
        "CompanyName",
        parent=company_style,
        fontName="Helvetica-Bold",
        fontSize=12,
        textColor=PRIMARY_GREEN
    )

    section_heading = ParagraphStyle(
        "SectionHeading",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=10,
        leading=14,
        textColor=PRIMARY_GREEN
    )

    client_name_style = ParagraphStyle(
        "ClientName",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=11,
        leading=14,
        textColor=BODY_TEXT
    )

    body_style = ParagraphStyle(
        "Body",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9.5,
        leading=12,
        textColor=BODY_TEXT
    )

    # --------------------------------------------------
    # HEADER SECTION
    # --------------------------------------------------

    left_header = [
        Paragraph("INVOICE", title_style),
        Paragraph(f"Id {id}", invoice_meta_style),
        Paragraph(f"Date: {invoice[1]}", invoice_meta_style)
    ]

    right_header = [
        Paragraph(request.form.get("company_name"), company_name_style),
        Paragraph(request.form.get("company_address"), company_style),
        Paragraph(request.form.get("gst_number"), company_style),
        Paragraph(request.form.get("company_phone"), company_style),
        Paragraph(request.form.get("company_email"), company_style)]

    header_table = Table(
        [[left_header, right_header]],
        colWidths=[printable_width / 2, printable_width / 2]
    )

    header_table.setStyle(
        TableStyle([
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("BOX", (0, 0), (-1, -1), 0, colors.white),
            ("LEFTPADDING", (0, 0), (-1, -1), 0),
            ("RIGHTPADDING", (0, 0), (-1, -1), 0)
        ])
    )

    story.append(header_table)
    story.append(Spacer(1, 12))

    # --------------------------------------------------
    # DECORATIVE RULE
    # --------------------------------------------------

    divider = Table(
        [[""]],
        colWidths=[printable_width]
    )

    divider.setStyle(
        TableStyle([
            ("LINEBELOW", (0, 0), (-1, -1), 1, DIVIDER)
        ])
    )

    story.append(divider)
    story.append(Spacer(1, 15))

    # --------------------------------------------------
    # BILL TO SECTION
    # --------------------------------------------------

    story.append(
        Paragraph(
            "BILL TO:",
            section_heading
        )
    )

    story.append(Spacer(1, 5))

    story.append(
        Paragraph(
            invoice[2],
            client_name_style
        )
    )

    story.append(
        Paragraph(
            invoice[3],
            body_style
        )
    )

    story.append(
        Paragraph(
            f"Phone: {invoice[4]}",
            body_style
        )
    )

    story.append(
        Paragraph(
            f"Email: {invoice[5]}",
            body_style
        )
    )

    story.append(Spacer(1, 18))

    # --------------------------------------------------
    # PRODUCT TABLE
    # --------------------------------------------------

    table_data = [
        [
            Paragraph("<b>Product</b>", body_style),
            Paragraph("<b>Qty</b>", body_style),
            Paragraph("<b>Rate</b>", body_style),
            Paragraph("<b>Total</b>", body_style)
        ]
    ]

    for item in products:

        table_data.append([
            Paragraph(item[2], body_style),
            Paragraph(str(item[3]), body_style),
            Paragraph(f"Rs. {item[4]:.2f}", body_style),
            Paragraph(f"Rs. {item[5]:.2f}", body_style)
        ])

    product_table = Table(
        table_data,
        colWidths=[
            printable_width * 0.50,
            printable_width * 0.15,
            printable_width * 0.15,
            printable_width * 0.20
        ]
    )

    product_table.setStyle(
        TableStyle([

            ("BACKGROUND",
             (0, 0),
             (-1, 0),
             TABLE_TINT),

            ("FONTNAME",
             (0, 0),
             (-1, 0),
             "Helvetica-Bold"),

            ("TEXTCOLOR",
             (0, 0),
             (-1, -1),
             BODY_TEXT),

            ("FONTSIZE",
             (0, 0),
             (-1, -1),
             9),

            ("LEFTPADDING",
             (0, 0),
             (-1, -1),
             6),

            ("RIGHTPADDING",
             (0, 0),
             (-1, -1),
             6),

            ("TOPPADDING",
             (0, 0),
             (-1, -1),
             6),

            ("BOTTOMPADDING",
             (0, 0),
             (-1, -1),
             6),

            ("ALIGN",
             (0, 0),
             (0, -1),
             "LEFT"),

            ("ALIGN",
             (1, 0),
             (-1, -1),
             "RIGHT"),

            ("VALIGN",
             (0, 0),
             (-1, -1),
             "MIDDLE"),

            ("LINEBELOW",
             (0, 0),
             (-1, -1),
             0.5,
             DIVIDER)

        ])
    )

    story.append(product_table)

    story.append(Spacer(1, 18))

    # --------------------------------------------------
    # TOTALS SECTION
    # --------------------------------------------------

    totals_data = [
    ["Subtotal", f"Rs. {invoice[6]:.2f}"],
    ["GST Tax", f"{invoice[7]:.2f}%"],
    ["Grand Total", f"Rs. {invoice[8]:.2f}"]
]

    totals_table = Table(
        totals_data,
        colWidths=[
            printable_width * 0.25,
            printable_width * 0.15
        ]
    )

    totals_table.setStyle(
        TableStyle([

            ("ALIGN",
             (0, 0),
             (-1, -1),
             "RIGHT"),

            ("TEXTCOLOR",
             (0, 0),
             (-1, -1),
             BODY_TEXT),

            ("FONTNAME",
             (0, 0),
             (-1, 1),
             "Helvetica"),

            ("FONTNAME",
             (0, 2),
             (-1, 2),
             "Helvetica-Bold"),

            ("FONTSIZE",
             (0, 2),
             (-1, 2),
             11),

            ("TEXTCOLOR",
             (0, 2),
             (-1, 2),
             PRIMARY_GREEN),

            ("LINEABOVE",
             (0, 2),
             (-1, 2),
             1,
             PRIMARY_GREEN)

        ])
    )

    wrapper = Table(
        [["", totals_table]],
        colWidths=[
            printable_width * 0.60,
            printable_width * 0.40
        ]
    )

    wrapper.setStyle(
        TableStyle([
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("BOX", (0, 0), (-1, -1), 0, colors.white)
        ])
    )

    story.append(wrapper)

    # --------------------------------------------------
    # BUILD PDF
    # --------------------------------------------------

    pdf.build(story)

    print("Invoice PDF generated.")

   

if __name__=='__main__':
   app.run()