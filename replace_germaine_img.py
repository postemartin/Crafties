import os
from docx import Document
from docx.shared import Inches

# Paths
docx_path = '/Users/posty/Documents/Arthur-and-Germaine/Arthur_and_Germaine_editable.docx'
new_img_path = '/Users/posty/.hermes/profiles/crafties/cache/images/img_771d30821f11.jpg'
output_path = '/Users/posty/Documents/Arthur-and-Germaine/Arthur_and_Germaine_editable.docx'

doc = Document(docx_path)

# Find the image in Chapter 2
target_found = False
image_to_replace = None

# Word images are in inline_shapes
# We need to find the one that is spatially/logically near Chapter 2.
# Since we can't easily map inline_shapes to paragraphs, 
# we can iterate through the document's XML elements.

# A simpler approach for this specific book:
# Chapter 2 starts around paragraph 36. 
# Let's look for the image that appears after that.

# We will use the relationship IDs.
for shape in doc.inline_shapes:
    # This is tricky. Let's try to find the image in the XML.
    pass

# Alternative: Use the image mapping we had earlier.
# I'll try to find the image in the XML that follows the "Chapter 2" text.
from docx.oxml.shared import qn

found_chapter = False
for para in doc.paragraphs:
    if "Chapter 2 — Then Came Germaine" in para.text:
        found_chapter = True
    
    if found_chapter:
        # Check if this paragraph contains an image (drawing)
        if para._element.xpath('.//w:drawing'):
            # Found the first image after Chapter 2!
            # Now we need to replace the image blob.
            # The drawing contains a blip with an rId.
            blip = para._element.xpath('.//a:blip')
            if blip:
                rid = blip[0].get('{http://schemas.openxmlformats.org/officeDocument/2006/relationships}embed')
                print(f"Found image with rId {rid} in paragraph: {para.text}")
                
                # Replace the image in the document's part
                part = doc.part.related_parts[rid]
                with open(new_img_path, 'rb') as f:
                    part._blob = f.read()
                
                target_found = True
                break

if target_found:
    doc.save(output_path)
    print("Successfully replaced Germaine's picture on page 3.")
else:
    print("Could not find the image to replace.")
