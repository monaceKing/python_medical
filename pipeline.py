from utils.dicom_loader import load_dicom
from corrections.attenuation import attenuation_correction
from corrections.movement import register_images

def process_image(
    ref_path,
    mov_path=None,
    apply_attenuation=True,
    apply_motion=True,
    config=None
):
    """
    Pipeline complet de traitement d'image scintigraphique.
    Fonction appelée par le système médical intégré.

    Paramètres:
    -----------
    ref_path : str
        Chemin vers l'image principale.
    mov_path : str | None
        Chemin vers l'image secondaire (pour la correction de mouvement).
    apply_attenuation : bool
        Active la correction d'atténuation.
    apply_motion : bool
        Active la correction de mouvement.
    config : dict
        Paramètres généraux.

    Retour:
    -------
    ref_corr : np.ndarray
        Image corrigée d'atténuation
    aligned : np.ndarray | None
        Image corrigée du mouvement
    """

    # 1) Chargement de l’image principale
    img_ref, meta_ref = load_dicom(ref_path)

    # 2) Correction d’atténuation
    if apply_attenuation:
        img_ref = attenuation_correction(img_ref, config)

    # 3) Correction de mouvement (si deuxième image fournie)
    aligned = None
    if apply_motion and mov_path is not None:
        aligned = register_images(ref_path, mov_path, config)

        # Si atténuation activée → appliquer aussi sur l’image alignée
        if apply_attenuation:
            aligned = attenuation_correction(aligned, config)

    return img_ref, aligned
