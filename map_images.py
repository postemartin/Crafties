from docx import Document
from docx.enum.shape import WD_INLINE_SHAPE

doc = Document('/Users/posty/Documents/Arthur-and-Germaine/Arthur_and_Germaine_editable.docx')

print("Image Mapping:")
image_count = 0
for i, para in enumerate(doc.paragraphs):
    # Check for inline shapes in the paragraph
    # Note: inline_shapes are at the document level, not paragraph level in python-docx
    pass

# Better way: iterate through all inline shapes and try to find which paragraph they belong to
# Actually, python-docx doesn't make it easy to link InlineShape to Paragraph.
# Let's just list the inline shapes and the text of the document to guess.
for shape in doc.inline_shapes:
    image_count += 1
    print(f"Image {image_count}: {shape.width}x{shape.height}")

# Let's try to find images by iterating through the XML or using the relationship IDs.
