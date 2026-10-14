from docx import Document
from docx.oxml.shared import qn

doc = Document('/Users/posty/Documents/Arthur-and-Germaine/Arthur_and_Germaine_editable.docx')
for i, para in enumerate(doc.paragraphs):
    # Check for page breaks in the paragraph
    for run in para.runs:
        if 'w:br' in run._element.xml and 'type="page"' in run._element.xml:
            print(f'Page break found in paragraph {i}: "{para.text}"')
    
    if '— Arthur —' in para.text:
        print(f'Speaker "— Arthur —" found at index {i}')
    if "I'm exercising." in para.text:
        print(f'Dialogue "I\'m exercising." found at index {i}')
