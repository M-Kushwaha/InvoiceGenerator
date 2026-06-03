# Invoice Generator

A web-based invoice generator built using Flask, MySQL, and ReportLab.

## Features

- Create invoices through a web interface
- Store invoice data in MySQL
- Dynamic invoice item management using JavaScript
- Responsive frontend using HTML, CSS, and JavaScript
- PDF invoice generation (Currently in Progress)

## Technologies Used

- Python
- Flask
- MySQL
- HTML
- CSS
- JavaScript
- ReportLab

## Project Status

🚧 Work in Progress

Completed:
- Invoice creation form
- Backend processing with Flask
- MySQL database integration
- Dynamic item handling

Under Development:
- PDF invoice generation
- UI improvements and styling

## Installation

1. Clone the repository

```bash
git clone https://github.com/M-Kushwaha/InvoiceGenerator.git
```

2. Move into the project directory

```bash
cd InvoiceGenerator
```

3. Create and activate a virtual environment

```bash
python -m venv venv
```

4. Install dependencies

```bash
pip install -r requirements.txt
```

5. Configure MySQL database

Update database credentials in `app.py`.

6. Run the application

```bash
python app.py
```

## Folder Structure

```text
InvoiceGenerator/
│
├── app.py
├── requirements.txt
├── templates/
├── static/
└── README.md
```

## Future Enhancements

- Download invoices as PDF
- Improved UI/UX
- User authentication

## Author

Meenu Kushwaha