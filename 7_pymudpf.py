import fitz
import requests


url = "https://www.italaw.com/sites/default/files/case-documents/italaw170490.pdf"
filename="RSM Production Corporation and others v. Grenada, ICSID Case No. ARB-10-6_Award.pdf"


response = requests.get(url)
response.raise_for_status()  # Check for any errors during the request

with open(filename, "wb") as file:
    file.write(response.content)


doc=fitz.open(filename)
out = open("/home/ubuntu/pdf_to_html/RSM Production Corporation and others v. Grenada, ICSID Case No. ARB-10-6_Award.txt", "wb") # create a text output

print(doc.page_count)
print(doc.get_toc(simple=False))


for page in doc: # iterate the document pages
	text = page.get_text("html").encode("utf8") # get plain text (is in UTF-8)
	print(page.get_text("text"))
	out.write(text) # write text of page
	out.write(bytes((12,))) # write page delimiter (form feed 0x0C)
out.close()
