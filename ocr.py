import pytesseract
from PIL import Image
import cv2
import numpy as np
import re

# Caminho do Tesseract no Windows — não muda se instalou no local padrão
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def pre_processar_imagem(imagem_bytes: bytes) -> np.ndarray:
    """
    Melhora a imagem antes de passar pro OCR.
    Converte para escala de cinza, aumenta contraste e remove ruído.
    """
    # Converte bytes para imagem OpenCV
    nparr = np.frombuffer(imagem_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # Escala de cinza
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Aumenta o tamanho (melhora muito a leitura de rótulos pequenos)
    scale = 2
    gray = cv2.resize(gray, None, fx=scale, fy=scale, interpolation=cv2.INTER_CUBIC)

    # Remove ruído
    gray = cv2.GaussianBlur(gray, (3, 3), 0)

    # Aumenta contraste (binarização adaptativa)
    gray = cv2.adaptiveThreshold(
        gray, 255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        11, 2
    )

    return gray


def extrair_texto_imagem(imagem_bytes: bytes) -> str:
    """
    Recebe os bytes de uma imagem e retorna o texto extraído pelo OCR.
    """
    img_processada = pre_processar_imagem(imagem_bytes)

    # Converte para PIL (formato que o pytesseract aceita)
    img_pil = Image.fromarray(img_processada)

    # Roda o OCR em português e inglês (ingredientes costumam ser em inglês/INCI)
    texto = pytesseract.image_to_string(img_pil, lang="por+eng")

    return texto


def extrair_ingredientes_do_texto(texto: str) -> str:
    """
    Tenta encontrar a lista de ingredientes no texto extraído.
    Procura pela palavra 'Ingredientes' ou 'Ingredients' e pega o que vem depois.
    """
    # Tenta achar a seção de ingredientes
    padrao = re.search(
        r"(?:ingredientes|ingredients)\s*[:\-]?\s*(.+)",
        texto,
        re.IGNORECASE | re.DOTALL
    )

    if padrao:
        ingredientes = padrao.group(1)
    else:
        # Se não achar o cabeçalho, retorna tudo (o usuário pode ajustar)
        ingredientes = texto

    # Limpa quebras de linha e espaços extras
    ingredientes = " ".join(ingredientes.split())

    # Remove caracteres estranhos comuns em OCR ruim
    ingredientes = re.sub(r"[|\\{}\[\]<>]", "", ingredientes)

    return ingredientes.strip()


def processar_foto_rotulo(imagem_bytes: bytes) -> dict:
    """
    Função principal: recebe a foto e retorna os ingredientes extraídos.
    """
    try:
        texto_bruto = extrair_texto_imagem(imagem_bytes)
        ingredientes = extrair_ingredientes_do_texto(texto_bruto)

        return {
            "sucesso": True,
            "ingredientes": ingredientes,
            "texto_completo": texto_bruto
        }
    except Exception as e:
        return {
            "sucesso": False,
            "ingredientes": "",
            "erro": str(e)
        }