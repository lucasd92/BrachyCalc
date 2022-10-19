from reportlab.pdfgen.canvas import Canvas
from reportlab.lib import colors
from reportlab.platypus import BaseDocTemplate, Frame, Paragraph, PageBreak, \
    PageTemplate, Spacer, FrameBreak, NextPageTemplate, Image, Table, TableStyle
from reportlab.lib.pagesizes import letter, A4, landscape
from reportlab.lib.units import inch, cm
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_CENTER,TA_LEFT


def print_report(report_header, table, file_name ):


    canvas = Canvas(file_name, pagesize=landscape(A4))

    doc = BaseDocTemplate(file_name)
    contents =[]
    width,height = A4

    left_header_frame = Frame(
        0.2*inch, 
        height-1.7*inch, 
        2*inch, 
        1.5*inch
        )

    right_header_frame = Frame(
        2.2*inch, 
        height-1.7*inch, 
        width-2.5*inch, 
        1.5*inch,id='normal'
        )

    frame_table_title= Frame(
        0.5*inch, 
        0.7*inch, 
        (width-0.6*inch)+0.17*inch, 
        height-2*inch,
        leftPadding = 0, 
        topPadding=0, 
        id='col'
        )

    frame_table= Frame(
        0.2*inch, 
        0.7*inch, 
        (width-0.6*inch)+0.17*inch, 
        height-2.5*inch,
        leftPadding = 0, 
        topPadding=0, 
        id='col'
        )

    laterpages = PageTemplate(id='laterpages',frames=[left_header_frame, right_header_frame,frame_table_title,frame_table],)

    logoleft = Image(report_header.logo_path)
    logoleft._restrictSize(2*inch, 2*inch)
    logoleft.hAlign = 'CENTER'
    logoleft.vAlign = 'CENTER'

    styleSheet = getSampleStyleSheet()
    style_title = styleSheet['Heading1']
    style_title.fontSize = 18 
    style_title.fontName = 'Helvetica-Bold'
    style_title.alignment=TA_CENTER

    style_data = styleSheet['Normal']
    style_data.fontSize = 14 
    style_data.fontName = 'Helvetica'
    style_data.alignment=TA_CENTER

    style_table_title = styleSheet['BodyText']
    style_table_title.fontSize = 14
    style_table_title.fontName = 'Helvetica'
    style_table_title.alignment=TA_LEFT

    canvas.setTitle(report_header.document_title)


    title_background = colors.fidblue


    table_data = report_header.table_header

    i = 0
    table_group= []
    size = len(table)

    count = 0
    # Genera la tabla
    for i in range(size):

        table_data.append([i, table[i][0], table[i][1], table[i][2], table[i][3], ' '])

        i += 1

        # table group es cada una de las páginas
        if ((i%20==0) or (i== size) ):

            table_actividades = Table(table_data, colWidths=85, rowHeights=30, repeatRows=1)
            tblStyle = TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), title_background),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ])

            rowNumb = len(table_data)
            #Alterna el color
            for row in range(1, rowNumb):
                if row % 2 == 0:
                    table_background = colors.lightblue
                else:
                    table_background = colors.aliceblue

                tblStyle.add('BACKGROUND', (0, row), (-1, row), table_background)

            table_actividades.setStyle(tblStyle)

            table_group.append(table_actividades)
            table_data = report_header.table_header


    contents.append(NextPageTemplate('laterpages'))

    for table in table_group:

        contents.append(logoleft)
        contents.append(FrameBreak())
        contents.append(Paragraph(report_header.main_title, style_title))
        contents.append(Paragraph(report_header.sub_title, style_data))
        contents.append(Paragraph(report_header.aditional_data, style_data))
        contents.append(FrameBreak())
        contents.append(Paragraph(report_header.table_title, style_table_title)) 
        contents.append(FrameBreak())
        contents.append(table)
        contents.append(FrameBreak())

    doc.addPageTemplates([laterpages,])
    doc.build(contents)