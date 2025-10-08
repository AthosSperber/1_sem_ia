import os
import cv2
import numpy as np
from PIL import Image
from tensorflow import keras
from keras.models import load_model

from dataset import load_images_from_folder, generate_patches
from cnn_model import build_cnn


def desenha_contorno_unico(img, patch_size, positions, preds, threshold=0.3):
    """
    Desenha um único retângulo ao redor da região que contém flores.
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
        (255, 0, 255),
        3
    )
    return img


def menu(model_path):
    """
    Menu simples para escolher a ação desejada.
    """
    if os.path.exists(model_path):
        print("\n📁 Modelo salvo encontrado.")
        print("[1] Treinar e SALVAR por cima do modelo atual")
        print("[2] Treinar mas NÃO salvar (modo temporário)")
        print("[3] Usar o modelo salvo (sem treinar)")
        opcao = input("\nEscolha uma opção (1/2/3): ").strip()
        return opcao
    else:
        print("\n🚀 Nenhum modelo salvo encontrado.")
        print("[1] Treinar e SALVAR novo modelo")
        print("[2] Treinar mas NÃO salvar (modo temporário)")
        opcao = input("\nEscolha uma opção (1/2): ").strip()
        return opcao


def main():
    base_path = os.path.dirname(os.path.abspath(__file__))
    flowers_path = os.path.join(base_path, "images", "flowers")
    non_flowers_path = os.path.join(base_path, "images", "non_flowers")
    test_folder = os.path.join(base_path, "images", "test")
    results_folder = os.path.join(base_path, "results")
    model_folder = os.path.join(base_path, "model")
    model_path = os.path.join(model_folder, "cnn_model.h5")
    patch_size = (32, 32)

    os.makedirs(results_folder, exist_ok=True)
    os.makedirs(model_folder, exist_ok=True)

    # Menu inicial
    opcao = menu(model_path)

    cnn = None

    # === Treinar e salvar ===
    if opcao == "1":
        print("\n🧠 Treinando modelo (será salvo após o treino)...")
        flowers = load_images_from_folder(flowers_path, label=1)
        non_flowers = load_images_from_folder(non_flowers_path, label=0)
        all_images = flowers + non_flowers

        if not all_images:
            print("[ERRO] Nenhuma imagem encontrada para treino.")
            return

        X, y = generate_patches(all_images, patch_size)
        if X.shape[0] == 0:
            print("[ERRO] Nenhum patch foi gerado.")
            return

        X = X.astype('float32') / 255.0
        X = X.reshape(-1, patch_size[0], patch_size[1], 3)

        cnn = build_cnn((patch_size[0], patch_size[1], 3))
        cnn.fit(X, y, epochs=500, batch_size=64, verbose=1)

        cnn.save(model_path)
        print(f"\n✅ Modelo salvo em: {model_path}")

    # === Treinar sem salvar ===
    elif opcao == "2":
        print("\n🧠 Treinando modelo (modo temporário)...")
        flowers = load_images_from_folder(flowers_path, label=1)
        non_flowers = load_images_from_folder(non_flowers_path, label=0)
        all_images = flowers + non_flowers

        if not all_images:
            print("[ERRO] Nenhuma imagem encontrada para treino.")
            return

        X, y = generate_patches(all_images, patch_size)
        if X.shape[0] == 0:
            print("[ERRO] Nenhum patch foi gerado.")
            return

        X = X.astype('float32') / 255.0
        X = X.reshape(-1, patch_size[0], patch_size[1], 3)

        cnn = build_cnn((patch_size[0], patch_size[1], 3))
        cnn.fit(X, y, epochs=20, batch_size=64, verbose=1)
        print("\n⚠️ Treinamento concluído, mas modelo não será salvo.")

    # === Usar modelo salvo ===
    elif opcao == "3" and os.path.exists(model_path):
        print("\n📦 Carregando modelo salvo...")
        cnn = load_model(model_path)
        print("✅ Modelo carregado com sucesso.")

    else:
        print("[ERRO] Opção inválida. Encerrando.")
        return

    # === Testar nas imagens ===
    if cnn is None:
        print("[ERRO] Nenhum modelo disponível para testar.")
        return

    if not os.path.exists(test_folder):
        print("[ERRO] Pasta de teste não encontrada.")
        return

    print("\n🔍 Iniciando predições nas imagens de teste...\n")

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

            img = desenha_contorno_unico(img, patch_size, positions, preds, threshold=0.3)
            img = img.astype(np.uint8)
            img_bgr = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

            save_path = os.path.join(results_folder, f"resultado_{test_img_name}")
            cv2.imwrite(save_path, img_bgr)
            print(f"[OK] Resultado salvo em {save_path}")

    print("\n✅ Processamento finalizado. Resultados estão na pasta 'results/'.")


if __name__ == "__main__":
    main()
