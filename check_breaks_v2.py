from docx import Document
from docx.oxml.shared import qn

doc = Document('/Users/posty/Documents/Arthur-and-Germaine/Arthur_and_Germaine_editable.docx')
page_count = 1
print(f"Page {page_count}:")

for i, para in enumerate(doc.paragraphs):
    # Check for page breaks in runs
    for run in para.runs:
        if 'w:br' in run._element.xml and 'type="page"' in run._element.xml:
            page_count += 1
            print(f"--- PAGE BREAK at para {i} ---")
            print(f"Page {page_count}:")
    
    # Check for section breaks (which also cause page breaks)
    if para._element.xpath('.//w:sectPr'):
        page_count += 1
        print(f"--- SECTION BREAK at para {i} ---")
        print(f"Page {page_count}:")

    if '— Arthur —' in para.text:
        print(f"  [Para {i}] {para.text}")
    if "I'm exercising." in para.text:
        print(f"  [Para {i}] {para.text}")
