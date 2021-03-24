import os
import PyPDF2

from PIL import Image
from fpdf import FPDF

def object_to_image(image_object, save_path):
    size = (image_object['/Width'], image_object['/Height'])
    #data = xObject[obj].getObject()
    data = image_object._data

    if image_object['/ColorSpace'] == '/DeviceRGB':
        mode = "RGB"
    else:
        mode = "P"

    if image_object['/Filter'] == '/FlateDecode':
        img = Image.frombytes(mode, size, data)
        img.save(f"{save_path}.png")
    elif image_object['/Filter'] == '/DCTDecode':
        img = open(f"{save_path}.jpg", "wb")
        img.write(data)
        img.close()
    elif image_object['/Filter'] == '/JPXDecode':
        img = open(f"{save_path}.jp2", "wb")
        img.write(data)
        img.close()

def page_to_image(page, save_path):
    try:
        xObject = page['/Resources']['/XObject'].getObject()

        for obj in xObject:
            if xObject[obj]['/Subtype'] == '/Image':
                object_to_image(xObject[obj], save_path)
    except:
        return


def pdf_to_images(path):
    filepath, filename = os.path.split(path)
    filename = filename.split('.')[0]
    save_folder = os.path.join(filepath, filename)
    
    if not os.path.exists(save_folder):
        os.mkdir(save_folder)

    pdf = PyPDF2.PdfFileReader(open(path, 'rb'))

    for page_num in range(pdf.getNumPages()):
        page = pdf.getPage(page_num)
        page_num = str(page_num)
        while len(page_num) < 4:
            page_num = "0" + page_num
        save_path = os.path.join(save_folder, page_num)

        page_to_image(page, save_path)

def imagelist_to_pdf(imagelist):
    pdf = FPDF()

    for image in imagelist:
        pdf.add_page()
        pdf.image(image, x=0, y=0, w=pdf.w, h=pdf.h)
    pdf.output("yourfile.pdf", "F")

#pdf_to_images("./sample.pdf")

#imagelist = ["sample/0.jpg","sample/10.jpg","sample/20.jpg"]
#imagelist_to_pdf(imagelist)

#pdf_to_images("pdf/sample.pdf")
#pdf_to_images("art.pdf")