import tkinter as tk
from tkinter import filedialog
import fitz  # PyMuPDF
import pytesseract
from PIL import Image
import io
import os

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def selecionar_pdfs():
    """Abre uma janela para selecionar múltiplos PDFs."""
    root = tk.Tk()
    root.withdraw()
    return filedialog.askopenfilenames(
        title="Selecione os PDFs",
        filetypes=[("Arquivos PDF", "*.pdf")]
    )

def extrair_texto_pdf(caminho_pdf):
    """Extrai texto de PDFs, incluindo imagens (OCR)."""
    try:
        doc = fitz.open(caminho_pdf)
        
        for pagina_num in range(len(doc)):
            pagina = doc.load_page(pagina_num)
            print(f"\n--- Página {pagina_num + 1} ---")

            # 1. Tenta extrair texto diretamente (PDFs nativos)
            texto_pagina = pagina.get_text()
            if texto_pagina.strip():
                print("[Texto nativo encontrado]\n")
                print(texto_pagina)
                continue

            # 2. Caso contrário, tenta OCR das imagens
            imagens = pagina.get_images(full=True)
            if not imagens:
                print("[Nenhuma imagem encontrada para OCR]")
                continue

        for img_index, img in enumerate(imagens):
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]

            # Converte para imagem Pillow
            image = Image.open(io.BytesIO(image_bytes))

            # Corrige rotação com base na orientação da página
            rotacao = int(pagina.rotation)
            if rotacao != 0:
                image = image.rotate(-rotacao, expand=True)

            # Executa OCR
            texto_ocr = pytesseract.image_to_string(image, lang='por+eng')

            print(f"\n[OCR da Imagem {img_index + 1}]\n")
            print(texto_ocr)

            # Exibe imagem já rotacionada
            image.show()

    except Exception as e:
        print(f"Erro ao processar {os.path.basename(caminho_pdf)}: {e}")

def main():
    print("Selecione os arquivos PDF para extração de texto...")
    caminhos_pdf = selecionar_pdfs()

    if not caminhos_pdf:
        print("Nenhum arquivo selecionado.")
        return

    for caminho_pdf in caminhos_pdf:
        print(f"\nProcessando: {os.path.basename(caminho_pdf)}...")
        extrair_texto_pdf(caminho_pdf)

if __name__ == "__main__":
    main()
