"""
[*] PDF [*] [*] [*]

[*] [*] [*] [*] PDF [*] [*].

[*] [*]:
    pip install reportlab
"""

import os

try:
    from reportlab.lib.pagesizes import letter, A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
    from reportlab.lib import colors
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
except ImportError:
    print("[ERROR] reportlab[*] [*] [*].")
    print("[*] [*]: pip install reportlab")
    exit(1)


def create_simple_pdf(output_path):
    """
    [*] [*] PDF [*]

    Args:
        output_path (str): [*] PDF [*]
    """
    try:
        # [*] [*]
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        # PDF [*] [*]
        doc = SimpleDocTemplate(output_path, pagesize=A4)

        # [*] [*]
        story = []

        # [*] [*]
        styles = getSampleStyleSheet()
        title_style = styles['Title']
        heading_style = styles['Heading1']
        normal_style = styles['Normal']

        # [*]
        story.append(Paragraph("Python PDF Parsing Tutorial", title_style))
        story.append(Spacer(1, 0.3 * inch))

        # [*] 1
        story.append(Paragraph("1. Introduction", heading_style))
        story.append(Spacer(1, 0.2 * inch))

        intro_text = """
        This is a sample PDF document created for practicing PDF parsing with Python.
        PDF (Portable Document Format) is a file format developed by Adobe that presents
        documents in a manner independent of application software, hardware, and operating systems.
        """
        story.append(Paragraph(intro_text, normal_style))
        story.append(Spacer(1, 0.3 * inch))

        # [*] 2
        story.append(Paragraph("2. Key Features", heading_style))
        story.append(Spacer(1, 0.2 * inch))

        features_text = """
        <b>Text Extraction:</b> Extract plain text from PDF documents.<br/>
        <b>Metadata Access:</b> Read document properties like author, title, and dates.<br/>
        <b>Page Manipulation:</b> Split, merge, and rotate PDF pages.<br/>
        <b>Table Extraction:</b> Parse structured table data from PDF files.
        """
        story.append(Paragraph(features_text, normal_style))
        story.append(Spacer(1, 0.3 * inch))

        # [*] 3 - [*]
        story.append(Paragraph("3. Python PDF Libraries", heading_style))
        story.append(Spacer(1, 0.2 * inch))

        # [*] [*]
        table_data = [
            ['Library', 'Strengths', 'Best For'],
            ['PyPDF2', 'Simple API, PDF manipulation', 'Basic text extraction'],
            ['pdfplumber', 'Table extraction, Layout', 'Complex documents'],
            ['PyMuPDF', 'High performance, Images', 'Large files'],
        ]

        # [*] [*]
        table = Table(table_data, colWidths=[1.5*inch, 2.5*inch, 2*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))

        story.append(table)
        story.append(Spacer(1, 0.3 * inch))

        # [*] [*]
        story.append(PageBreak())

        # [*] 2
        story.append(Paragraph("4. Sample Content for Testing", heading_style))
        story.append(Spacer(1, 0.2 * inch))

        sample_text = """
        This page contains sample text for practicing text extraction.
        You can use various Python libraries to parse this content.

        Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod
        tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam,
        quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.

        <b>Important:</b> Always verify the extracted text for accuracy.
        Some PDFs may have encoding issues or non-standard fonts that can affect extraction quality.
        """
        story.append(Paragraph(sample_text, normal_style))
        story.append(Spacer(1, 0.3 * inch))

        # [*] [*]
        code_style = ParagraphStyle(
            'Code',
            parent=normal_style,
            fontName='Courier',
            fontSize=9,
            leftIndent=20,
            rightIndent=20,
            spaceAfter=10,
            textColor=colors.darkblue,
            backColor=colors.lightgrey,
        )

        code_text = """
import PyPDF2

with open('document.pdf', 'rb') as file:
    reader = PyPDF2.PdfReader(file)
    text = reader.pages[0].extract_text()
    print(text)
        """

        story.append(Paragraph("Code Example:", heading_style))
        story.append(Spacer(1, 0.1 * inch))
        story.append(Paragraph(code_text.replace('\n', '<br/>'), code_style))

        # PDF [*]
        doc.build(story)

        print(f"[OK] [*] PDF [*] [*]: {output_path}")

    except Exception as e:
        print(f"[ERROR] PDF [*] [*]: {e}")


def create_table_pdf(output_path):
    """
    [*] [*] PDF [*]

    Args:
        output_path (str): [*] PDF [*]
    """
    try:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        doc = SimpleDocTemplate(output_path, pagesize=A4)
        story = []
        styles = getSampleStyleSheet()

        # [*]
        story.append(Paragraph("Sales Report - Q4 2025", styles['Title']))
        story.append(Spacer(1, 0.3 * inch))

        # [*]
        story.append(Paragraph("Monthly Sales Data", styles['Heading2']))
        story.append(Spacer(1, 0.2 * inch))

        # [*] [*]
        sales_data = [
            ['Month', 'Product A', 'Product B', 'Product C', 'Total'],
            ['October', '1,200', '850', '1,450', '3,500'],
            ['November', '1,350', '920', '1,580', '3,850'],
            ['December', '1,800', '1,100', '2,000', '4,900'],
            ['Total', '4,350', '2,870', '5,030', '12,250'],
        ]

        # [*] [*]
        table = Table(sales_data, colWidths=[1.2*inch, 1.2*inch, 1.2*inch, 1.2*inch, 1.2*inch])
        table.setStyle(TableStyle([
            # [*] [*]
            ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),

            # [*] [*] [*]
            ('BACKGROUND', (0, 1), (-1, -2), colors.lightblue),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),

            # [*] [*] [*]
            ('BACKGROUND', (0, -1), (-1, -1), colors.lightgrey),
            ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
        ]))

        story.append(table)
        story.append(Spacer(1, 0.5 * inch))

        # [*] [*]
        story.append(Paragraph("Regional Distribution", styles['Heading2']))
        story.append(Spacer(1, 0.2 * inch))

        regional_data = [
            ['Region', 'Sales', 'Growth %'],
            ['North', '4,500', '+12%'],
            ['South', '3,200', '+8%'],
            ['East', '2,800', '+15%'],
            ['West', '1,750', '+5%'],
        ]

        table2 = Table(regional_data, colWidths=[2*inch, 2*inch, 2*inch])
        table2.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.green),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BACKGROUND', (0, 1), (-1, -1), colors.lightgreen),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))

        story.append(table2)

        # PDF [*]
        doc.build(story)

        print(f"[OK] [*] PDF [*] [*]: {output_path}")

    except Exception as e:
        print(f"[ERROR] [*] PDF [*] [*]: {e}")


def main():
    """
    [*] [*]: [*] [*] PDF [*]
    """
    print("=" * 60)
    print("[*] PDF [*] [*]")
    print("=" * 60)

    # [*] [*]
    output_dir = "data"

    # 1. [*] PDF
    print("\n1. [*] [*] PDF [*] [*]...")
    create_simple_pdf(f"{output_dir}/sample.pdf")

    # 2. [*] PDF
    print("\n2. [*] [*] PDF [*] [*]...")
    create_table_pdf(f"{output_dir}/sample_table.pdf")

    print("\n" + "=" * 60)
    print("[OK] [*] [*] PDF [*] [*]!")
    print("=" * 60)

    print("\n[*] [*]:")
    print(f"  - {output_dir}/sample.pdf")
    print(f"  - {output_dir}/sample_table.pdf")

    print("\n[*] [*] [*] [*] [*] [*] [*]:")
    print("  python 01_basic_pdf_parser.py")
    print("  python 02_text_extractor.py")
    print("  python 03_table_extractor.py")


if __name__ == "__main__":
    main()
