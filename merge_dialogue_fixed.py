from docx import Document

docx_path = '/Users/posty/Documents/Arthur-and-Germaine/Arthur_and_Germaine_editable.docx'
doc = Document(docx_path)

# We need to iterate backwards when deleting paragraphs to avoid index shifts
i = len(doc.paragraphs) - 2
while i >= 0:
    para = doc.paragraphs[i]
    next_para = doc.paragraphs[i+1]
    
    if "— Arthur —" in para.text and "I'm exercising." in next_para.text:
        # Combine the text. 
        # Since we are replacing the whole paragraph text, we use a simple join.
        # Note: .text replacement removes formatting. 
        # To keep formatting, we should append a run.
        
        # Get the text of the second paragraph
        text_to_append = next_para.text
        
        # Add a newline and the text to the first paragraph
        para.add_run().add_break()
        para.add_run(text_to_append)
        
        # Remove the second paragraph
        p = next_para._element
        p.getparent().remove(p)
        print(f"Merged dialogue at index {i}")
    i -= 1

doc.save(docx_path)
print("Saved changes.")
