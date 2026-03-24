import pypdf
import os
from pathlib import Path

# Arquivo de entrada e saída
input_pdf = "Catalogo-JLA.pdf"
output_pdf = "Catalogo-JLA-reduzido.pdf"

print(f"Comprimindo {input_pdf}...")
print(f"Tamanho original: {os.path.getsize(input_pdf) / (1024*1024):.2f} MB")

# Abrir o PDF e criar um writer
reader = pypdf.PdfReader(input_pdf)
writer = pypdf.PdfWriter()

# Copiar todas as páginas
for page in reader.pages:
    writer.add_page(page)

# Comprimir conteúdo
for page in writer.pages:
    page.compress_content_streams()

# Adicionar metadados
if reader.metadata:
    writer.add_metadata(reader.metadata)

# Salvar com compressão máxima
with open(output_pdf, "wb") as output_file:
    writer.write(output_file)

print(f"✓ PDF comprimido salvo como: {output_pdf}")
print(f"Tamanho final: {os.path.getsize(output_pdf) / (1024*1024):.2f} MB")
print(f"Redução: {(1 - os.path.getsize(output_pdf) / os.path.getsize(input_pdf)) * 100:.1f}%")
