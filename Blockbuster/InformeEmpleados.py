import sys
from conexionBD import ConexionBD
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Spacer
from reportlab.lib import colors
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.piecharts import Pie
from reportlab.graphics.charts.textlabels import Label
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph
from reportlab.lib.enums import TA_CENTER


def create_pdf(datos,tarta,tarta2):
    datos.insert(0,('ID','DNI', 'Nombre','Apellidos','Clientes atendidos este mes','Salario','Turno'))
    
    # Create a PDF document
    pdf = SimpleDocTemplate("InformeEmpleados.pdf", pagesize=A4)
    elements = []

    custom_title_style = ParagraphStyle(
        'CustomTitleStyle',
        fontName='Helvetica',
        alignment=TA_CENTER,
        fontSize=24,
        leading=18,
        spaceAfter=12
        )
    custom_style = ParagraphStyle(
        'CustomStyle',
        fontName='Helvetica',
        fontSize=12,
        leading=15,
        )
    
    title = Paragraph("Informe de los empleados de la taquillera.",custom_title_style)
    text = Paragraph("Estas dos ruedas muestran cuántos clientes fueron atendidos y el rendimiento del local según su numero de empleados.",custom_style)
    
    # Create a table
    table = Table(datos)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0),colors.Color(red=(26/255),green=(26/255),blue=(26/255))),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.gold),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1),colors.Color(red=(46/255),green=(46/255),blue=(46/255))),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.whitesmoke),
        ('GRID', (0, 0), (-1, -1), 1, colors.Color(red=(26/255),green=(26/255),blue=(26/255))),
    ]))

    drawing = Drawing(800, 400)
    pie = Pie()
    pie.x = 20
    pie.y = 200
    values = [row[1] for row in tarta[0:]]  # Skip the header row
    labels = [row[0] for row in tarta[0:]]   
    pie.data = values
    pie.labels = labels
    pie.sideLabels = 1
    pie.slices.strokeWidth = 0.5
    drawing.add(pie)
    lab = Label()
    lab.setOrigin (85,335)
    lab.setText ('Esta rueda muestra los Clientes que atendió cada empleado.')
    drawing.add(lab)

    pie2 = Pie()
    pie2.x = 280
    pie2.y = 200
    values2 = [row[0] for row in tarta2[0:]]
    labels2 = ['Matutino','Vespertino','Nocturno']   
    pie2.data = values2
    pie2.labels = labels2
    pie2.sideLabels = 1
    pie2.slices.strokeWidth = 0.5
    drawing.add(pie2)
    lab2 = Label()
    lab2.setOrigin (335,335)
    lab2.setText ('Esta rueda muestra qué empleados trabajan en cada turno.')
    drawing.add(lab2)

    elements.append(title)
    elements.append(Spacer(1, 15))
    elements.append(table)
    elements.append(Spacer(1, 30))
    elements.append(text)
    elements.append(drawing)
    pdf.build(elements)