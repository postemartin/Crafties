from docx import Document

docx_path = '/Users/posty/Documents/Arthur-and-Germaine/Arthur_and_Germaine_editable.docx'
doc = Document(docx_path)

found = False
for para in doc.paragraphs:
    if "🥬❤️" in para.text:
        # We find the position of the heart emoji
        text = para.text
        idx = text.rfind("❤️")
        if idx != -1:
            # Keep everything up to and including the heart
            # and remove anything that comes after it in that paragraph.
            # If the symbol is in the same paragraph:
            new_text = text[:idx+1] # heart is 1 char in python if it's one glyph, but emojis can be tricky
            # Let's be safer: find the emoji and slice.
            # Actually, let's just use the user's description: "after the lettuce and heart emoji"
            
            # Let's check if there's actually anything after it.
            after = text[idx+1:]
            if after:
                print(f"Found trailing characters: {repr(after)}")
                para.text = text[:idx+1]
                found = True
            else:
                print("Nothing found after heart emoji in this paragraph.")

# Also check the very next paragraph to see if it's a standalone symbol.
# Since we are in a loop, we can't easily do 'next' without indices.
# Let's restart the loop with indices.

doc = Document(docx_path)
for i in range(len(doc.paragraphs)):
    para = doc.paragraphs[i]
    if "🥬❤️" in para.text:
        if i + 1 < len(doc.paragraphs):
            next_para = doc.paragraphs[i+1]
            # If the next paragraph is very short (e.g., 1-2 chars) and not a normal word, it might be the symbol.
            if 0 < len(next_para.text) < 3:
                print(f"Found suspicious next paragraph: {repr(next_para.text)}")
                # Remove the paragraph
                p = next_para._element
                p.getparent().remove(p)
                found = True

if found:
    doc.save(docx_path)
    print("Removed the symbol.")
else:
    print("Symbol not found.")
