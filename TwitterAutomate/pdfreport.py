# Python libraries
from fpdf import FPDF
from matplotlib.pyplot import plot
from datetime import datetime, timedelta

width = 210
height = 297

def create_title(day, pdf):
    pdf.set_font('Courier', 'B', 24)
    pdf.ln(60)
    pdf.write(5, f"Twitter Sentiment Report")
    pdf.ln(10)
    pdf.set_font('Courier', 'B', 16)
    pdf.write(4,f'{day}')
    pdf.ln(5)

def create_report(day, filename='/home/andy/Documents/PythonExercises/TwitterAutomate/TweetsReport.pdf'):
    pdf = FPDF()
    """"First Page"""
    pdf.add_page()
    pdf.image("./resources/header.jpeg", -3, 0, width)
    create_title(day, pdf)
    pdf.image("./TweetsAnalized.png", 5, 110, width-20)
    pdf.output(filename)

if __name__ == '__main__':
    day = (datetime.today() - timedelta(days=1)).strftime("%m/%d/%y").replace("/0", "/").lstrip("0")
    create_report(day)