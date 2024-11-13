import os
import cv2
import streamlit as st
from pathlib import Path
import torch
import pickle
from PIL import Image
import numpy as np
import pandas as pd
#from yolov5 import YOLO
import seaborn as sns
import tensorflow as tf
import pathlib
import pytesseract
import matplotlib.pyplot as plt
from tensorflow.keras.preprocessing.image import img_to_array
import easyocr  # Certifique-se de importar o EasyOCR

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

reader = easyocr.Reader(['en'])  # Substitua 'en' pelo idioma adequado, se necessário

temp = pathlib.PosixPath
pathlib.PosixPath = pathlib.WindowsPath
st.title("YOLO Detecção de Objetos com Streamlit")

def preprocess_image(image):
    if isinstance(image, np.ndarray):  # Se já for um array NumPy
        image = Image.fromarray(image)
    
    # Redimensionar a imagem
    image = image.resize((224, 224))
    
    # Converter para array NumPy e normalizar
    image_array = np.array(image) / 255.0
    
    # Expandir dimensões para corresponder à entrada esperada pelo modelo
    image_array = image_array.reshape(1, 224, 224, 3)     
    return image_array


def visualizar_pickle(cropped_head_resized, temperatura_calculada, segmented_head):
    # Verificar se a imagem tem 3 dimensões (imagem colorida)
    # if cropped_head_resized.ndim == 3:
    #     st.image(cropped_head_resized, caption='Imagem da Cabeça Recortada', use_column_width=True)
    # else:
    #     st.image(cropped_head_resized, caption='Imagem da Cabeça Recortada (Escala de Cinza)', use_column_width=True)

    # Mostrar a imagem segmentada
    st.image(segmented_head[:, :], clamp=True)

    #st.image(, caption='Imagem Segmentada', use_column_width=True)

    # Mostrar as imagens
    st.write(f"[DEBUG] Temperatura calculada: {temperatura_calculada:.2f} °C")
    st.text(f"Temperatura calculada: {temperatura_calculada:.2f} °C")

# Define the dice loss function
def dice_loss(y_true, y_pred):
    smooth = 1.
    y_true_f = K.flatten(y_true)
    y_pred_f = K.flatten(y_pred)
    intersection = K.sum(y_true_f * y_pred_f)
    return 1 - (2. * intersection + smooth) / (K.sum(y_true_f) + K.sum(y_pred_f) + smooth)

# Register the custom loss function
@tf.keras.utils.register_keras_serializable()
def dice_loss(y_true, y_pred):
    return dice_loss(y_true, y_pred)

def iou_metric(y_true, y_pred):
    intersection = tf.reduce_sum(tf.cast(y_true * y_pred, tf.float32))
    union = tf.reduce_sum(tf.cast(y_true + y_pred - y_true * y_pred, tf.float32))
    return intersection / union

# Carregar o modelo de segmentação
def load_segmentation_model():
    model = tf.keras.models.load_model('modelo_segmentacao.keras')  # Substitua pelo caminho correto
    return model

# Carregar o modelo YOLO a partir do arquivo .pt
def load_yolo_model():
    st.write("[DEBUG] Carregando o modelo YOLO...")
    model_path = 'best.pt'  # Substitua pelo caminho correto do seu arquivo .pt
    st.write(f"[DEBUG] Caminho do modelo YOLO: {model_path}")
    model = torch.hub.load('yolov5', 'custom', path='best.pt', source='local', force_reload=True)
    st.write("[DEBUG] Modelo YOLO carregado com sucesso.")
    return model

# Função para fazer upload do vídeo
def upload_video():
    st.write("[DEBUG] Iniciando upload do vídeo...")
    uploaded_file = st.file_uploader("Upload um vídeo", type=["mp4", "avi", "mov", "mkv"])
    if uploaded_file is not None:
        video_path = "video.mp4"
        with open(video_path, "wb") as f:
            f.write(uploaded_file.read())
        st.write(f"[DEBUG] Vídeo carregado com sucesso: {video_path}")
        return video_path
    st.write("[DEBUG] Nenhum vídeo foi carregado.")
    return None

# Função para processar o vídeo e salvar frames
def process_video(video_path, output_dir, capture_fps=1.5):
    st.write(f"[DEBUG] Iniciando processamento do vídeo: {video_path}")
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        st.error("Erro ao abrir o vídeo.")
        st.write("[DEBUG] Falha ao abrir o vídeo.")
        return []

    original_fps = cap.get(cv2.CAP_PROP_FPS)
    st.write(f"[DEBUG] FPS original do vídeo: {original_fps}")
    frame_interval = int(original_fps / capture_fps)
    st.write(f"[DEBUG] Intervalo de frames: {frame_interval}")
    frame_count = 0
    saved_frames = []

    os.makedirs(output_dir, exist_ok=True)
    st.write(f"[DEBUG] Diretório de saída criado: {output_dir}")

    while True:
        ret, frame = cap.read()
        if not ret:
            st.write("[DEBUG] Fim do vídeo ou erro ao ler o frame.")
            break

        if frame_count % frame_interval == 0:
            frame_filename = os.path.join(output_dir, f'frame_{frame_count:04d}.png')
            cv2.imwrite(frame_filename, frame)
            saved_frames.append(frame_filename)
            st.write(f"[DEBUG] Frame salvo: {frame_filename}")

        frame_count += 1

    cap.release()
    st.write("[DEBUG] Processamento do vídeo concluído.")
    return saved_frames

def salvar_pickle(frame_path, head_image, segmented_image, temperatura, pickle_output_path):
    data = {
        "frame_original": frame_path,  # Para referência, o caminho do frame original
        "imagem_cabeca": head_image,  # Imagem da cabeça recortada e redimensionada
        "imagem_segmentada": segmented_image,  # Imagem segmentada retornada pelo modelo
        "grade_temperatura": temperatura  # Valor de temperatura calculado
    }
    with open(pickle_output_path, 'wb') as f:
        pickle.dump(data, f)
    st.write(f"[DEBUG] Dados serializados no arquivo pickle: {pickle_output_path}")

# Função para extrair a temperatura da grade
def extrair_grade_pixels(image):
    
    image_path = 'frame_9766.png'
    image = cv2.imread(image_path)

    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    bar_region = gray_image[:, -50:]

    min_val = np.min(bar_region)
    max_val = np.max(bar_region)
      
    return min_val, max_val

def extrair_grade_temperatura(image):
    # Extrair o texto da imagem usando EasyOCR

    image_path = 'frame_9766.png'
    image = cv2.imread(image_path)

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)

    text = pytesseract.image_to_string(thresh, config='--psm 6')

    # Imprimir o texto extraído
    print("Texto extraído:")
    print(text)

    import re

    pattern = r"\d{2}\.\d{2}"

    temperaturas = re.findall(pattern, text)

    print("Temperaturas encontradas:")
    print(temperaturas)
    
    temp_min = float(temperaturas[0])
    temp_max = float(temperaturas[1])

    return temp_min, temp_max

def media_pixels(segmented_head):
    pixels_not_black= segmented_head[segmented_head > 0]

    pixels_ordered= np.sort(pixels_not_black)

    pixels_ordered_reverse= pixels_ordered[::-1]

    pixels_10_percent= pixels_ordered_reverse[:int(len(pixels_ordered_reverse)*0.1)]
    print(f"10% dos pixels mais escuros: {pixels_10_percent}")

    print(len(pixels_ordered))
    media_pixelss= np.mean(pixels_10_percent)
    print(f"Média dos pixels que não são pretos: {media_pixelss}")
    return media_pixelss
# Função para processar o frame, detectar a cabeça e realizar segmentação

resultados = []

def processar_frame(yolo_model, segmentation_model, frame_path, output_dir):
    frame = Image.open(frame_path)  # Carregar o frame usando PIL.Image
    frame_np = np.array(frame)
    st.write(f"[DEBUG] Realizando inferência no frame: {frame_path}")
    
    # Realizar inferência com YOLO
    results = yolo_model(frame_np)
    img_with_boxes = np.array(results.render()[0])  # Desenhar bounding boxes

    crop_id = 1

    # Recortar a cabeça detectada e redimensionar
    for (*box, conf, cls) in results.xyxy[0]:
        x_min, y_min, x_max, y_max = map(int, box)
        cropped_head = frame_np[y_min:y_max, x_min:x_max]
        cropped_head = Image.fromarray(cropped_head)

        # Redimensionar a cabeça recortada para 128x128
        image = cropped_head.resize((128, 128))  # Exemplo de redimensionamento, ajuste se necessário
        image_array = np.array(image)
        image_array = image_array / 255.0  # MANTER os valores normalizados entre 0 e 1

        # Ajustar a imagem para corresponder ao formato de entrada esperado pelo modelo
        # (por exemplo, adicionando a dimensão do batch)
        image_array = image_array.reshape(1, 128, 128, 3)  # Exemplo de ajuste, modifique conforme necessário
        
        # Realizar a predição de segmentação
        predicted_mask = segmentation_model.predict(image_array)
        predicted_mask = predicted_mask[0, :, :, 0]

        # Aqui desnormalizamos a máscara de predição para trazer de volta à escala de 0 a 255
        predicted_mask = predicted_mask * 255

        # Imprimir os valores mínimos e máximos corretamente desnormalizados
        print("Shape preview: ", predicted_mask.shape)
        print("Valores máximos e mínimos: ", np.min(predicted_mask), np.max(predicted_mask))

        min_val, max_val = extrair_grade_pixels(frame_path)
        temp_min, temp_max = extrair_grade_temperatura(frame_path)
        
        # Calcular a temperatura da cabeça com os valores desnormalizados
        media_pixelss = media_pixels(predicted_mask)
        
        # Calcular a temperatura usando a média dos pixels
        temperatura_calculada = ((media_pixelss - min_val) / (max_val - min_val)) * (temp_max - temp_min) + temp_min
        
        # Salvar os dados do frame, crop e temperatura
        resultados.append({
            "Frame": frame_path,
            "Cropped Head": f"crop_{Path(frame_path).stem}_id{crop_id}.png",  # Nome do crop baseado no nome do frame
            "Temperature (°C)": temperatura_calculada
        })

        crop_id += 1 

        pickle_output_path = os.path.join(output_dir, f'frame_{Path(frame_path).stem}.pkl')
        visualizar_pickle(cropped_head, temperatura_calculada, predicted_mask)
        
        salvar_pickle(frame_path, cropped_head, predicted_mask, temperatura_calculada, pickle_output_path)

def gerar_dataframe_temperaturas():
    # Criar o dataframe com os dados coletados
    df_temperaturas = pd.DataFrame(resultados)
    return df_temperaturas
# Função principal
def run_inference_on_frames(yolo_model, segmentation_model, frames, output_dir):
    st.write("[DEBUG] Iniciando inferência nos frames...")
    os.makedirs(output_dir, exist_ok=True)

    for i, frame_path in enumerate(frames):
        processar_frame(yolo_model, segmentation_model, frame_path, output_dir)
    df_temperaturas = gerar_dataframe_temperaturas()
    st.write(df_temperaturas)
    plotar_distribuicao_temperaturas(df_temperaturas)

def plotar_distribuicao_temperaturas(df_temperaturas):
    plt.figure(figsize=(10, 6))
    sns.histplot(df_temperaturas['Temperature (°C)'], bins=10, kde=True)
    plt.title('Distribuição das Temperaturas Calculadas')
    plt.xlabel('Temperatura (°C)')
    plt.ylabel('Frequência')
    plt.grid(True)
    plt.show()


# Exemplos de uso
video_path = upload_video()
model_yolo = load_yolo_model()
model_segmentation = load_segmentation_model()

if video_path:
    st.write("Processando o vídeo...")
    output_dir = './frames/'
    frames = process_video(video_path, output_dir)

    if frames:
        st.write("Realizando inferência nos frames...")
        run_inference_on_frames(model_yolo, model_segmentation, frames, output_dir)
    else:
        st.write("[DEBUG] Nenhum frame foi processado.")
else:
    st.write("[DEBUG] Nenhum vídeo para processar.")