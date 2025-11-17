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

# -------------------------------------------------------------
# UTILISATEUR : définissez ici vos images DICOM
# -------------------------------------------------------------

# 1 seule image
single_image = r"C:\python_medical\images\frame1.dcm"

# 2 images (correction du mouvement)
ref = r"C:\python_medical\images\frame1.dcm"
mov = r"C:\python_medical\images\frame2.dcm"

# Plusieurs images (série dynamique)
multi_images = [
    r"C:\python_medical\images\frame1.dcm",
    r"C:\python_medical\images\frame2.dcm",
    r"C:\python_medical\images\frame3.dcm"
]

# -------------------------------------------------------------
# EXÉCUTION 1 : TRAITEMENT D’UNE SEULE IMAGE
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
