import os

from glob import glob

def get_dir_list(path):
    dirlist = [path]
    for d in dirlist:
        for filename in os.listdir(d):
            filepath = os.path.join(d, filename)
            if os.path.isdir(filepath):
                dirlist.append(filepath)
    return dirlist

def get_pdf_list(dirlist):
    filelist = []
    for d in dirlist:
        for filename in glob(os.path.join(d, "*.pdf")):
            filelist.append(filename)
    
    return filelist


src_path = "/data/Book/"
dirlist = get_dir_list(path)
pdflist = get_pdf_list(dirlist)

dst_path = "pdf_image"
temp = pdflist[40].split("/")
temp[0] = dst_path
temp = os.path.join(*temp)
print(temp)

