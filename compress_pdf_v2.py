import fitz  # PyMuPDF
import os

# Arquivo de entrada e saída
input_pdf = "Catalogo-JLA.pdf"
output_pdf = "Catalogo-JLA-reduzido.pdf"

print(f"Comprimindo {input_pdf}...")
print(f"Tamanho original: {os.path.getsize(input_pdf) / (1024*1024):.2f} MB")
print("Processando páginas (isso pode levar alguns minutos)...")

# Abrir o PDF
doc = fitz.open(input_pdf)

# Criar configurações de compressão agressiva
# deflate=1: compressão de conteúdo
# garbage=4: remover objetos não usados
# clean=1: limpar sintaxe
# deflate_images=1: comprimir imagens
# deflate_fonts=1: comprimir fontes
print(f"Total de páginas: {len(doc)}")

# Salvar com compressão máxima
doc.save(
    output_pdf,
    garbage=4,           # Maximum garbage collection
    clean=True,          # Clean up
    deflate=True,        # Compress streams
    deflate_images=True, # Compress images
    deflate_fonts=True,  # Compress fonts
)

doc.close()

print(f"✓ PDF comprimido salvo como: {output_pdf}")
print(f"Tamanho final: {os.path.getsize(output_pdf) / (1024*1024):.2f} MB")
reducao = (1 - os.path.getsize(output_pdf) / os.path.getsize(input_pdf)) * 100
print(f"Redução: {reducao:.1f}%")
