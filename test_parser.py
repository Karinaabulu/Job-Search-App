from cv_parser import extract_text, structure_cv

text = extract_text("uploads/98765432101_cv_English for Business Purposes.pdf")
structured = structure_cv(text)
print(structured)