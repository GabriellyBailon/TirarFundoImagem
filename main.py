import streamlit as st
import numpy as np
import cv2
from rembg import remove
from io import BytesIO
from PIL import Image

def remove_background(image: Image.Image):
    """Remove o fundo da imagem usando rembg."""
    return remove(image)

def image_to_svg(image: Image.Image):
    """Converte uma imagem para SVG detectando os contornos."""
    # Converte a imagem para escala de cinza
    gray = cv2.cvtColor(np.array(image), cv2.COLOR_RGBA2GRAY)
    
    # Converte a imagem para binária (preto e branco)
    _, binary = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY)
    
    # Encontra os contornos na imagem
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Cria um SVG manualmente
    svg_data = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {image.width} {image.height}">\n'
    for contour in contours:
        svg_data += '<path d="M '
        for point in contour:
            x, y = point[0]
            svg_data += f'{x},{y} '
        svg_data += 'Z" fill="black" stroke="none"/>\n'
    svg_data += '</svg>'
    
    return svg_data

# Interface do Streamlit
st.sidebar.title("Editor de Imagens")
option = st.sidebar.radio("Escolha uma opção", ["Remover Fundo"])

# Define o título conforme a opção escolhida
st.title("Remover Fundo")

# Upload de imagem
uploaded_file = st.file_uploader("Carregue uma imagem", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    image = Image.open(uploaded_file).convert("RGBA")
    
    # Barra de progresso
    progress = st.progress(0)
    
    if option == "Remover Fundo":
        progress.progress(50)
        no_bg = remove_background(image)
        progress.progress(100)
        st.image(no_bg, caption="Prévia da imagem", use_container_width=False, width=200)
        
        # Botão para baixar a imagem sem fundo abaixo da barra de progresso
        img_byte_arr = BytesIO()
        no_bg.save(img_byte_arr, format='PNG')
        st.download_button("Baixar imagem sem fundo", data=img_byte_arr.getvalue(), file_name="imagem_sem_fundo.png", mime="image/png")
    
    elif option == "Vetorizar Imagem":
        progress.progress(50)
        svg_output = image_to_svg(image)
        progress.progress(100)

        st.download_button("Baixar imagem vetorizada (SVG)", data=svg_output, file_name="imagem_vetorizada.svg", mime="image/svg+xml")

# Adicionando anúncios na lateral
st.sidebar.markdown("### Anúncio")
st.sidebar.markdown(
    """
    <div style="text-align:center;">
        <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js"></script>
        <ins class="adsbygoogle"
             style="display:block"
             data-ad-client="ca-pub-XXXXXXXXXXXXXXX"   # Substitua pelo seu ID de cliente do AdSense
             data-ad-slot="XXXXXXXXXX"                  # Substitua pelo seu ID do slot de anúncio
             data-ad-format="auto"></ins>
        <script>
             (adsbygoogle = window.adsbygoogle || []).push({});
        </script>
    </div>
    """,
    unsafe_allow_html=True
)

