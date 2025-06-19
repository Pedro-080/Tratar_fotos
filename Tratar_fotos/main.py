import tkinter as tk
from tkinter import filedialog
from pdf2image import convert_from_path
import pytesseract
import os

# Configuração do Tesseract (ajuste conforme seu sistema)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Windows

def selecionar_pdfs():
    root = tk.Tk()
    root.withdraw()  # Esconde a janela principal
    caminhos_pdf = filedialog.askopenfilenames(
        title="Selecione um ou mais PDFs",
        filetypes=[("Arquivos PDF", "*.pdf")]
    )
    return caminhos_pdf

def extrair_texto_pdf(caminho_pdf):
    imagens = convert_from_path(caminho_pdf)
    texto_extraido = ""
    
    for i, imagem in enumerate(imagens):
        temp_img_path = f"temp_page_{i+1}.jpg"
        imagem.save(temp_img_path, "JPEG")
        texto_pagina = pytesseract.image_to_string(imagem, lang='por')  # Ajuste o idioma
        texto_extraido += f"--- Página {i+1} ---\n{texto_pagina}\n\n"
        os.remove(temp_img_path)
    
    return texto_extraido

def main():
    print("Selecione um ou mais arquivos PDF...")
    caminhos_pdf = selecionar_pdfs()
    
    if not caminhos_pdf:
        print("Nenhum arquivo selecionado.")
        return
    
    for caminho_pdf in caminhos_pdf:
        print(f"\nProcessando: {os.path.basename(caminho_pdf)}")
        texto = extrair_texto_pdf(caminho_pdf)
        
        nome_saida = caminho_pdf.replace(".pdf", "_extraido.txt")
        with open(nome_saida, "w", encoding="utf-8") as arquivo_saida:
            arquivo_saida.write(texto)
        
        print(f"Texto extraído salvo em: {nome_saida}")

if __name__ == "__main__":
    main()