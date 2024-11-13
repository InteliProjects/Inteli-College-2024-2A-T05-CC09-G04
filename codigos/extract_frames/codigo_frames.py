import cv2
import os

# Caminho para o vídeo
video_path = 'C:\\Users\\Inteli\\Documents\\Inteli\\Modulo9\\Projeto\\video_08_08.mp4'

# Diretório onde os frames serão salvos
output_dir = 'C:\\Users\\Inteli\\Downloads\\frames_out_video_08_08_all_frames'
os.makedirs(output_dir, exist_ok=True)

capture_fps = 1.5

# Carrega o vídeo
cap = cv2.VideoCapture(video_path)

if not cap.isOpened():
    print("Erro ao abrir o vídeo.")
    exit()

# Obtém a taxa de fps do vídeo 
original_fps = cap.get(cv2.CAP_PROP_FPS)

# Calcula o intervalo de frames para atingir a taxa de captura desejada
frame_interval = int(original_fps / capture_fps)

print("Frame Int", frame_interval)

print("Original fps", original_fps)


frame_count = 0
saved_frame_count = 0

while True:
    # Lê o próximo frame
    ret, frame = cap.read()

    if not ret:
        break

    # Salva o frame se ele corresponder ao intervalo calculado
    if frame_count % frame_interval == 0:
        frame_filename = os.path.join(output_dir, f'frame_{saved_frame_count:04d}.png')
        cv2.imwrite(frame_filename, frame)
        saved_frame_count += 1

    frame_count += 1

# Libera o vídeo
cap.release()

print(f"Extração concluída! {saved_frame_count} frames foram salvos no diretório '{output_dir}'.")
