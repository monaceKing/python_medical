"""
main.py
-------
Point d'entrée principal pour tester le pipeline de correction
des artefacts en scintigraphie planaire.

Ce module montre :
- Comment traiter 1 image
- Comment traiter 2 images (correction du mouvement)
- Comment traiter N images (série dynamique)
"""

from pipeline import process_image
from config import config
import matplotlib.pyplot as plt
import os

# ⭐ CHEMINS RELATIFS - Plus besoin de modifier les chemins !
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGES_DIR = os.path.join(BASE_DIR, "images")

# -------------------------------------------------------------
# UTILISATEUR : définissez ici vos images DICOM
# -------------------------------------------------------------

# 1 seule image
single_image = os.path.join(IMAGES_DIR, "frame1.dcm")

# 2 images (correction du mouvement)
ref = os.path.join(IMAGES_DIR, "frame1.dcm")
mov = os.path.join(IMAGES_DIR, "frame2.dcm")

# Plusieurs images (série dynamique)
multi_images = [
    os.path.join(IMAGES_DIR, "frame1.dcm"),
    os.path.join(IMAGES_DIR, "frame2.dcm"),
    os.path.join(IMAGES_DIR, "frame3.dcm")
]

# Vérification des fichiers
def check_files_exist():
    """Vérifie que tous les fichiers DICOM existent"""
    all_files = [single_image, ref, mov] + multi_images
    for filepath in set(all_files):  # set() pour éviter les doublons
        if not os.path.exists(filepath):
            print(f"❌ ERREUR : Fichier introuvable : {filepath}")
            print(f"📁 Dossier images : {IMAGES_DIR}")
            print(f"📄 Fichiers disponibles : {os.listdir(IMAGES_DIR) if os.path.exists(IMAGES_DIR) else 'Dossier inexistant'}")
            exit(1)
    print("✅ Tous les fichiers DICOM ont été trouvés")

# Vérification avant de commencer
check_files_exist()

# -------------------------------------------------------------
# EXÉCUTION 1 : TRAITEMENT D'UNE SEULE IMAGE
# -------------------------------------------------------------

print("\n--- TRAITEMENT : 1 seule image ---")

ref_corr, _ = process_image(
    paths=single_image,
    apply_attenuation=True,
    apply_motion=False,
    config=config
)

plt.figure(figsize=(5,5))
plt.title("Image corrigée (Atténuation seule)")
plt.imshow(ref_corr, cmap="gray")
plt.show()

# -------------------------------------------------------------
# EXÉCUTION 2 : TRAITEMENT DE 2 IMAGES
# -------------------------------------------------------------

print("\n--- TRAITEMENT : 2 images (Atténuation + Mouvement) ---")

ref_corr, mov_corr = process_image(
    paths=[ref, mov],
    apply_attenuation=True,
    apply_motion=True,
    config=config
)

plt.figure(figsize=(10,5))

plt.subplot(1,2,1)
plt.title("Référence corrigée")
plt.imshow(ref_corr, cmap="gray")

plt.subplot(1,2,2)
if mov_corr is not None:
    plt.title("Alignée (Mouvement corrigé)")
    plt.imshow(mov_corr, cmap="gray")
else:
    plt.title("Aucune correction de mouvement")
plt.show()

# -------------------------------------------------------------
# EXÉCUTION 3 : TRAITEMENT DE N IMAGES
# -------------------------------------------------------------

print("\n--- TRAITEMENT : Plusieurs images (Série dynamique) ---")

ref_corr, aligned_list = process_image(
    paths=multi_images,
    apply_attenuation=True,
    apply_motion=True,
    config=config
)

plt.figure(figsize=(5,5))
plt.title("Image Référence corrigée (série dynamique)")
plt.imshow(ref_corr, cmap="gray")
plt.show()

if aligned_list:
    for idx, aligned in enumerate(aligned_list):
        plt.figure(figsize=(5,5))
        plt.title(f"Image alignée n°{idx+1}")
        plt.imshow(aligned, cmap="gray")
        plt.show()