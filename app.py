# importing Flask and other modules
from flask import Flask, request, render_template 
import mysql.connector as a

print("CONNECTING...")

mycon = a.connect(
  host="localhost",
  user="root",
  password="#12canossian",
  database="invoices",
  ssl_disabled =True
)
print("CONNECTED")

cursor = mycon.cursor()
app = Flask(__name__)   

# A decorator used to tell the application
# which URL is associated function
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

if __name__=='__main__':
   app.run()