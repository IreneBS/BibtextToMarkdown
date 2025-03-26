import os
import re
import bibtexparser
from datetime import datetime

def clean_title(title):
    """Convierte el título en un formato válido para permalink."""
    return re.sub(r'[^a-zA-Z0-9]+', '_', title).lower().strip('_')

def extract_date(entry):
    """Genera la fecha en formato YYYY-MM-DD."""
    year = entry.get("year", "0000")
    month = entry.get("month", "01")
    day = entry.get("day", "01")
    
    if not month.isdigit():
        month = "01"
    if not day.isdigit():
        day = "01"
    
    return f"{year}-{int(month):02d}-{int(day):02d}"

def bibtex_to_markdown(input_file, output_folder):
    """Convierte cada entrada de un archivo BibTeX en archivos Markdown individuales."""
    with open(input_file, "r", encoding="utf-8") as bibfile:
        bib_database = bibtexparser.load(bibfile)
    
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    for entry in bib_database.entries:
        title = entry.get("title", "Sin título").strip()
        venue = entry.get("journal", entry.get("booktitle", "Desconocido")).strip()
        date = extract_date(entry)
        key = entry.get("ID", clean_title(title))
        permalink = f"{clean_title(key)}.md"
        
        markdown_content = f"""---
title: "{title}"
collection: "publications"
category: "manuscripts"
permalink: "{permalink}"
excerpt: ""
date: "{date}"
venue: "{venue}"
---
"""
        
        output_path = os.path.join(output_folder, permalink)
        with open(output_path, "w", encoding="utf-8") as md_file:
            md_file.write(markdown_content)
        
        print(f"Archivo generado: {output_path}")

# Ejemplo de uso
input_bibtex = "files/referencias.bib"  # Nombre del archivo BibTeX
output_directory = "output_markdown"  # Carpeta de salida
bibtex_to_markdown(input_bibtex, output_directory)
