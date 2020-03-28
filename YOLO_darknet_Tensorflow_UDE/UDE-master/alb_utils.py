from tkinter import Tk
from tkinter.filedialog import askopenfilename

Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
filename = askopenfilename() # show an "Open" dialog box and return the path to the selected file
print(filename)

def alb_collab_to_pdf(filename): 
  os.system('apt-get install texlive texlive-xetex texlive-latex-extra pandoc')
  os.system('pip install pypandoc')
  os.system('jupyter nbconvert --to PDF'+filename)
