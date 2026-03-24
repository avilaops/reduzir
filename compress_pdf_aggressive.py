import fitz  # PyMuPDF
import os
from PIL import Image
import io

# Arquivo de entrada e saída
input_pdf = "Catalogo-JLA.pdf"
output_pdf = "Catalogo-JLA-reduzido.pdf"

# Configurações de qualidade (ajuste conforme necessário)
DPI = 150  # Reduzir para 150 DPI (original provavelmente é 300)
JPEG_QUALITY = 70  # Qualidade JPEG (0-100, menor = mais compressão)

print(f"Comprimindo {input_pdf}...")
print(f"Tamanho original: {os.path.getsize(input_pdf) / (1024*1024):.2f} MB")
print(f"Configurações: {DPI} DPI, Qualidade JPEG: {JPEG_QUALITY}%")
print("Processando páginas (isso pode levar alguns minutos)...")

# Abrir o PDF original
doc_original = fitz.open(input_pdf)
doc_novo = fitz.open()  # Criar novo PDF vazio

total_paginas = len(doc_original)

for i, pagina in enumerate(doc_original):
    print(f"  Processando página {i+1}/{total_paginas}...", end='\r')
    
    # Renderizar página como imagem com DPI reduzido
    mat = fitz.Matrix(DPI/72, DPI/72)  # 72 é DPI padrão
    pix = pagina.get_pixmap(matrix=mat)
    
    # Converter para PIL Image
    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
    
    # Comprimir como JPEG
    img_bytes = io.BytesIO()
    img.save(img_bytes, format='JPEG', quality=JPEG_QUALITY, optimize=True)
    img_bytes.seek(0)
    
    # Obter dimensões originais da página
    rect = pagina.rect
    
    # Criar nova página e inserir imagem comprimida
    nova_pagina = doc_novo.new_page(width=rect.width, height=rect.height)
    nova_pagina.insert_image(rect, stream=img_bytes.read())

print(f"\n  Salvando arquivo comprimido...")

# Salvar o novo PDF
doc_novo.save(output_pdf, garbage=4, deflate=True)
doc_original.close()
doc_novo.close()

print(f"✓ PDF comprimido salvo como: {output_pdf}")
print(f"Tamanho final: {os.path.getsize(output_pdf) / (1024*1024):.2f} MB")
reducao = (1 - os.path.getsize(output_pdf) / os.path.getsize(input_pdf)) * 100
print(f"Redução: {reducao:.1f}%")
print(f"\nEconomia de espaço: {(os.path.getsize(input_pdf) - os.path.getsize(output_pdf)) / (1024*1024):.2f} MB")
