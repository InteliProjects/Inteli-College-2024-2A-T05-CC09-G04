import os
import cv2
import xml.etree.ElementTree as ET
import numpy as np
import random
import re

# Função para ajustar as coordenadas e pintar o label da cabeça
def pintar_cabeca_recortada(root, mask, new_xtl, new_ytl, scale_x, scale_y):
    for box in root.findall(".//box[@label='cabeca']"):
        xtl = int((float(box.get('xtl')) - new_xtl) * scale_x)
        ytl = int((float(box.get('ytl')) - new_ytl) * scale_y)
        xbr = int((float(box.get('xbr')) - new_xtl) * scale_x)
        ybr = int((float(box.get('ybr')) - new_ytl) * scale_y)
        mask[ytl:ybr, xtl:xbr] = [255, 255, 255]  # Pintar a cabeça de branco

# Função para ajustar as coordenadas e pintar o label dos olhos
def pintar_olho_recortado(root, mask, new_xtl, new_ytl, scale_x, scale_y):
    for box in root.findall(".//box[@label='olho']"):
        xtl = int((float(box.get('xtl')) - new_xtl) * scale_x)
        ytl = int((float(box.get('ytl')) - new_ytl) * scale_y)
        xbr = int((float(box.get('xbr')) - new_xtl) * scale_x)
        ybr = int((float(box.get('ybr')) - new_ytl) * scale_y)
        mask[ytl:ybr, xtl:xbr] = [0, 0, 255]  # Pintar o olho de vermelho

# Função para obter os fatores de expansão com base na configuração
def get_expansion_factors(config):
    factors = [
        (0.15, 0.25, 0.15, 0.25),
        (0.1, 0.3, 0.25, 0.15),
        (0.25, 0.15, 0.2, 0.2),
        (0.3, 0.1, 0.2, 0.2),
        (0.2, 0.2, 0.15, 0.25),
        (0.2, 0.2, 0.25, 0.15),
        (0.15, 0.25, 0.2, 0.2),
        (0.25, 0.15, 0.25, 0.15),
        (0.1, 0.3, 0.3, 0.1),
        (0.3, 0.1, 0.15, 0.25),
        (0.2, 0.2, 0.1, 0.3),
        (0.2, 0.2, 0.3, 0.1),
        (0.15, 0.25, 0.3, 0.1),
        (0.25, 0.15, 0.1, 0.3),
        (0.1, 0.3, 0.2, 0.2),
        (0.3, 0.1, 0.25, 0.15),
        (0.25, 0.15, 0.15, 0.25),
        (0.2, 0.2, 0.2, 0.2)
    ]
    return factors[config - 1]

def processar_imagem_e_xml(pasta_base, xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    # Definição de variáveis conforme especificado
    data_dd_mm_yy = "08-08-2024"
    video_i = 1
    nome_original_video = "00000000215000500.mp4"
    numero_crop_j = 1

    for image_tag in root.findall('image'):
        image_name = image_tag.get("name")
        frame_name = os.path.basename(image_name) 
        frame_number_re = re.search(r'\d+', frame_name)
        frame_number= frame_number_re.group(0)

        print("Processando a imagem", frame_number)

        config = random.randint(1, 18)
        
        # Definir os fatores de expansão com base na configuração selecionada
        left_expansion, right_expansion, top_expansion, bottom_expansion = get_expansion_factors(config)

        image_path = os.path.join(pasta_base, frame_name)
        image = cv2.imread(image_path)

        if image is None:
            raise ValueError(f"Erro ao carregar a imagem em {image_path}")

        for box in image_tag.findall(".//box[@label='cabeca']"):
            xtl = float(box.get('xtl'))
            ytl = float(box.get('ytl'))
            xbr = float(box.get('xbr'))
            ybr = float(box.get('ybr'))
            
            # Expande o bounding box para incluir mais contexto ao redor
            width = xbr - xtl
            height = ybr - ytl
            
            new_xtl = max(0, int(xtl - width * left_expansion))
            new_ytl = max(0, int(ytl - height * top_expansion))
            new_xbr = min(image.shape[1], int(xbr + width * right_expansion))
            new_ybr = min(image.shape[0], int(ybr + height * bottom_expansion))
            
            # Recortar a imagem original ao redor da cabeça com o contexto adicional
            cropped_image = image[new_ytl:new_ybr, new_xtl:new_xbr]
            
            # Redimensionar a imagem para 128x128
            resized_image = cv2.resize(cropped_image, (128, 128))
            
            # Salvar a imagem recortada e redimensionada na pasta X
            pasta_nome_x = "X_burle"
            if not os.path.exists(pasta_nome_x):
                os.makedirs(pasta_nome_x)
            output_filename_x = f"{data_dd_mm_yy}_video{video_i}_{nome_original_video}_{frame_number}_{numero_crop_j}_x.png"
            output_path_x = os.path.join(pasta_nome_x, output_filename_x)
            cv2.imwrite(output_path_x, resized_image)
            
            # Criar uma máscara em preto com o mesmo tamanho da imagem redimensionada
            mask = np.zeros_like(resized_image)
            
            # Calcular a escala entre as coordenadas originais e o novo tamanho
            scale_x = resized_image.shape[1] / (new_xbr - new_xtl)
            scale_y = resized_image.shape[0] / (new_ybr - new_ytl)
            
            # Pintar as regiões na máscara usando as funções ajustadas
            pintar_cabeca_recortada(image_tag, mask, new_xtl, new_ytl, scale_x, scale_y)
            pintar_olho_recortado(image_tag, mask, new_xtl, new_ytl, scale_x, scale_y)

            # Salvar a máscara pintada na pasta Y
            pasta_nome_y = "Y_burle"
            if not os.path.exists(pasta_nome_y):
                os.makedirs(pasta_nome_y)
            output_filename_y = f"{data_dd_mm_yy}_video{video_i}_{nome_original_video}_{frame_number}_{numero_crop_j}_y.png"
            output_path_y = os.path.join(pasta_nome_y, output_filename_y)
            cv2.imwrite(output_path_y, mask)
            
            print(f"Imagem pintada salva em {output_path_y}")
            print(f"Imagem original salva em {output_path_x}")

def main():
    # Defina o caminho base onde estão as pastas das vacas
    pasta_base = "C:\\Users\\Inteli\\Downloads\\pasta_burle"
    xml_file = os.path.join(pasta_base, "annotations.xml")
    print(f"Processando imagens e XMLs na pasta {pasta_base} com o arquivo XML {xml_file}")

    processar_imagem_e_xml(pasta_base, xml_file)

if __name__ == "__main__":
    main()
