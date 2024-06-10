import sys
from conexionBD import ConexionBD
from reportlab.lib.pagesizes import A3
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle , Spacer
from reportlab.lib import colors
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.piecharts import Pie
from reportlab.graphics.charts.textlabels import Label
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph
from reportlab.lib.enums import TA_CENTER

def create_pdf(datos,tarta,tarta2,tarta3,tarta4,tarta5):
    datos.insert(0,('ID', 'Título','Presupuesto','Recaudaciones','Director','Actores','Oscares','Razzis','Nominaciones'))
    
    # Create a PDF document
    pdf = SimpleDocTemplate("InformePelis.pdf", pagesize=A3)
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
    
    title = Paragraph("Informe de datos de las películas de la taquillera.",custom_title_style)
    text = Paragraph("Estos cuadros de rueda comparan diversos datos de las películas.",custom_style)
     
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
    pie.x = 50
    pie.y = 200
    values = [row[1] for row in tarta[0:]]  # Skip the header row
    labels = [row[0] for row in tarta[0:]]   
    pie.data = values
    pie.labels = labels
    pie.sideLabels = 1
    pie.slices.strokeWidth = 0.5
    drawing.add(pie)
    lab = Label()
    lab.setOrigin (135,335)
    lab.setText ('Esta rueda muestra los presupuestos de realizar cada película.')
    drawing.add(lab)

    pie2 = Pie()
    pie2.x = 450
    pie2.y = 200
    values2 = [row[1] for row in tarta2[0:]]  # Skip the header row
    labels2 = [row[0] for row in tarta2[0:]]   
    pie2.data = values2
    pie2.labels = labels2
    pie2.sideLabels = 1
    pie2.slices.strokeWidth = 0.5
    drawing.add(pie2)
    lab2 = Label()
    lab2.setOrigin (525,335)
    lab2.setText ('Esta rueda muestra las recaudaciones de las ventas de cada película.')
    drawing.add(lab2)

    pie3 = Pie()
    pie3.x = 50
    pie3.y = -150
    values3 = [row[1] for row in tarta3[0:]]  # Skip the header row
    labels3 = [row[0] for row in tarta3[0:]]   
    pie3.data = values3
    pie3.labels = labels3
    pie3.sideLabels = 1
    pie3.slices.strokeWidth = 0.5
    drawing.add(pie3)
    lab3 = Label()
    lab3.setOrigin (335,160)
    lab3.setText ('Esta rueda muestra cuantas veces fue la pelicula nominada a los Óscares')
    drawing.add(lab3)

    pie4 = Pie()
    pie4.x = 450
    pie4.y = -150
    values4 = [row[1] for row in tarta4[0:]]  # Skip the header row
    labels4 = [row[0] for row in tarta4[0:]]   
    pie4.data = values4
    pie4.labels = labels4
    pie4.sideLabels = 1
    pie4.slices.strokeWidth = 0.5
    drawing.add(pie4)
    lab4 = Label()
    lab4.setOrigin (115,-10)
    lab4.setText ('Esta rueda muestra cuantas veces ganó los Óscares')
    drawing.add(lab4)

    pie5 = Pie()
    pie5.x = 250
    pie5.y = 25
    values5 = [row[1] for row in tarta5[0:]]  # Skip the header row
    labels5 = [row[0] for row in tarta5[0:]]   
    pie5.data = values5
    pie5.labels = labels5
    pie5.sideLabels = 1
    pie5.slices.strokeWidth = 0.5
    drawing.add(pie5)
    lab5 = Label()
    lab5.setOrigin (500,-10)
    lab5.setText ('Esta rueda muestra cuantas veces ganó los Razzis')
    drawing.add(lab5)

    elements.append(title)
    elements.append(Spacer(1, 15))
    elements.append(table)
    elements.append(Spacer(1, 30))
    elements.append(text)
    elements.append(drawing)
    pdf.build(elements)