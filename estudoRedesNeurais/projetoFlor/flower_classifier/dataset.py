from PIL import Image
import numpy as np
import os

def load_images_from_folder(folder, label):
    """
    Carrega imagens de uma pasta e atribui um label.
    label = 1 -> flor
    label = 0 -> não flor
    """
    images = []
    if not os.path.exists(folder):
        print(f"[ERRO] Pasta não encontrada: {folder}")
        return images

    for filename in os.listdir(folder):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            img_path = os.path.join(folder, filename)
            try:
                img = Image.open(img_path).convert('RGB')
                img = np.array(img)
                images.append({'image': img, 'label': label})
                print(f"Carregada: {img_path} - shape: {img.shape}")
            except Exception as e:
                print(f"[ERRO] Falha ao carregar {img_path}: {e}")
    return images

def generate_patches(images, patch_size=(32, 32)):
    """
    Quebra cada imagem em patches de patch_size
    e retorna X (patches) e y (labels).
    """
    X, y = [], []
    for item in images:
        img = item['image']
        label = item['label']
        h, w = img.shape[:2]

        for i in range(0, h - patch_size[0] + 1, patch_size[0]):
            for j in range(0, w - patch_size[1] + 1, patch_size[1]):
                patch = img[i:i+patch_size[0], j:j+patch_size[1]]
                if patch.shape == (patch_size[0], patch_size[1], 3):
                    X.append(patch)
                    y.append(label)

    return np.array(X), np.array(y)  # y como vetor 1D (mais padrão)
