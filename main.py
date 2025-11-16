from pipeline import process_image
from config import config
import matplotlib.pyplot as plt

# Exemple d'utilisation
ref = "images/frame1.dcm"
mov = "images/frame2.dcm"

# ou bien par exemple 
# ref = r"C:\Users\juste\Desktop\images_medicales\patient1_ref.dcm"
# mov = r"C:\Users\juste\Desktop\images_medicales\patient1_mov.dcm"


# Traitement complet (atténuation + mouvement)
ref_corr, mov_corr = process_image(
    ref_path=ref,
    mov_path=mov,
    apply_attenuation=True,
    apply_motion=True,
    config=config
)

# Affichage
plt.subplot(1,2,1)
plt.title("Référence corrigée")
plt.imshow(ref_corr, cmap='gray')

plt.subplot(1,2,2)
plt.title("Mouvement corrigé")
plt.imshow(mov_corr, cmap='gray')

plt.show()
