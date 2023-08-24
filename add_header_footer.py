from PyPDF2 import PdfReader, PdfWriter
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from reportlab.lib import utils
from reportlab.pdfgen import canvas
from io import BytesIO

def add_header(input_pdf_path, output_pdf_path, header_image_path):
    # Load the input PDF file
    input_pdf = PdfReader(input_pdf_path)

    # Create a new PDF buffer with A3 size
    output_pdf_buffer = BytesIO()
    output_pdf = canvas.Canvas(output_pdf_buffer, pagesize=A4)

    # Resize and add header image
    header_image = utils.ImageReader(header_image_path)
    header_width, header_height = A4[0], inch * 3# Assuming a 2-inch header
    output_pdf.drawImage(header_image, 0, A4[1] - header_height, width=header_width, height=header_height)

    # Add a new page to the output PDF
    output_pdf.showPage()

    # Save the output PDF content in the buffer
    output_pdf.save()

    # Create a writer for the output PDF
    output_pdf_writer = PdfWriter()

    # Merge each page from the input PDF into the output PDF
    for page_num in range(len(input_pdf.pages)):
        page = input_pdf.pages[page_num]

        # Create a new PDF object with the current page and the header from the buffer
        new_pdf = PdfReader(output_pdf_buffer)
        new_page = new_pdf.pages[0]

        # Merge the header page with the current page
        page.merge_page(new_page)
        output_pdf_writer.add_page(page)

    # Save the merged output PDF file
    with open(output_pdf_path, "wb") as f:
        output_pdf_writer.write(f)

if __name__ == "__main__":
    input_pdf_path = "C:\\f_pdf\\input_pdf.pdf"     # Update with your input PDF path
    output_pdf_path = "C:\\f_pdf\\output_pdf.pdf"   # Update with the desired output path and use .pdf extension
    header_image_path = "C:\\f_pdf\\header_image.png"  # Update with the path to your header image

    add_header(input_pdf_path, output_pdf_path, header_image_path)

