import pypdfium2 as pdfium  # 4.0.0
from tqdm import tqdm  # 4.66.2
import os

scale = 3
path = 'paper.pdf'
pdf = pdfium.PdfDocument(path)
N = len(pdf)  # number of pages
n = len(str(N))  # digits of <N>

directory, filename = os.path.split(path)
basename, extension = os.path.splitext(filename)
if not os.path.exists(basename):  # create a folder as the pdf name
    os.mkdir(basename)

for idx in tqdm(range(N), total=N):
    counter = format(idx+1, '>0'+str(n))
    page_name = f"{basename}-{counter}.png"
    page_path = os.path.join(basename, page_name)
    page = pdf[idx]
    image = page.render(scale=scale).to_pil()
    image.save(page_path)
