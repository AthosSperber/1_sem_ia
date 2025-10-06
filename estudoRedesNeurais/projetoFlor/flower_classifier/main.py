import os
import cv2
import numpy as np
from PIL import Image

from dataset import load_images_from_folder, generate_patches
from cnn_model import build_cnn

def desenha_contorno_unico(img, patch_size, positions, preds, threshold= 0.7):
    """
    Desenha um único retângulo ao redor da região que contém flores
    (com base nas predições e limiar definido).
    """
    flower_indices = [idx for idx, p in enumerate(preds) if p >= threshold]
    if not flower_indices:
        return img

    min_i = min(positions[idx][0] for idx in flower_indices)
    min_j = min(positions[idx][1] for idx in flower_indices)
    max_i = max(positions[idx][0] for idx in flower_indices)
    max_j = max(positions[idx][1] for idx in flower_indices)

    cv2.rectangle(
        img,
        (min_j, min_i),
        (max_j + patch_size[1], max_i + patch_size[0]),
        (255, 0, 255),  # cor retangulo
        3
    )
    return img

def main():
    base_path = os.path.dirname(os.path.abspath(__file__))
    flowers_path = os.path.join(base_path, "images", "flowers")
    non_flowers_path = os.path.join(base_path, "images", "non_flowers")
    test_folder = os.path.join(base_path, "images", "test")
    results_folder = os.path.join(base_path, "results")
    patch_size = (32, 32)

    # Criar pasta results se não existir
    os.makedirs(results_folder, exist_ok=True)

    # Carregar imagens de treino
    flowers = load_images_from_folder(flowers_path, label=1)
    non_flowers = load_images_from_folder(non_flowers_path, label=0)
    all_images = flowers + non_flowers
    print(f"Total de imagens carregadas: {len(all_images)}")

    if len(all_images) == 0:
        print("[ERRO] Nenhuma imagem encontrada para treino.")
        return

    # Gerar patches
    X, y = generate_patches(all_images, patch_size=patch_size)
    print(f"Patches gerados: {X.shape[0]}")

    if X.shape[0] == 0:
        print("[ERRO] Nenhum patch foi gerado.")
        return

    # Normalização
    X = X.astype('float32') / 255.0

    # Ajustar shape para CNN
    X = X.reshape(-1, patch_size[0], patch_size[1], 3)

    # Criar e treinar CNN
    cnn = build_cnn((patch_size[0], patch_size[1], 3))
    cnn.fit(X, y, epochs=200, batch_size=64 , verbose=1)

    # Testar nas imagens da pasta test
    if not os.path.exists(test_folder):
        print("[ERRO] Pasta de teste não encontrada.")
        return

    for test_img_name in os.listdir(test_folder):
        if test_img_name.lower().endswith(('.png', '.jpg', '.jpeg')):
            img_path = os.path.join(test_folder, test_img_name)
            img = Image.open(img_path).convert('RGB')
            img = np.array(img)

            patches, positions = [], []
            h, w = img.shape[:2]
            for i in range(0, h - patch_size[0] + 1, patch_size[0]):
                for j in range(0, w - patch_size[1] + 1, patch_size[1]):
                    patch = img[i:i+patch_size[0], j:j+patch_size[1]]
                    if patch.shape == (patch_size[0], patch_size[1], 3):
                        patches.append(patch)
                        positions.append((i, j))

            if not patches:
                print(f"[AVISO] Nenhum patch válido em {test_img_name}")
                continue

            patches = np.array(patches).astype('float32') / 255.0
            preds = cnn.predict(patches, verbose=0).flatten()

            img = desenha_contorno_unico(img, patch_size, positions, preds, threshold= 0.7)
            img = img.astype(np.uint8)
            img_bgr = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

            # Salvar resultado
            save_path = os.path.join(results_folder, f"resultado_{test_img_name}")
            cv2.imwrite(save_path, img_bgr)
            print(f"[OK] Resultado salvo em {save_path}")

    print("✅ Processamento finalizado. Resultados estão na pasta 'results/'.")

if __name__ == "__main__":
    main()
