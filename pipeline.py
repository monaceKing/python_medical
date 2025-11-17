from utils.dicom_loader import load_dicom
from corrections.attenuation import attenuation_correction
from corrections.movement import register_images

def process_image(
    paths,
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

    # NORMALISATION DE L'ENTRÉE
    if isinstance(paths, str):
        paths = [paths]              # 1 seule image
    elif isinstance(paths, list):
        if len(paths) == 0:
            raise ValueError("Aucune image fournie.")
    else:
        raise TypeError("paths doit être un str ou une liste de chemins DICOM.")

    # CAS 1 : une seule image → pas de correction de mouvement
    if len(paths) == 1:
        img, _ = load_dicom(paths[0])

        if apply_attenuation:
            img = attenuation_correction(img, config)

        return img, None   # (image corrigée, pas d’image alignée)

    # CAS 2 : deux images → correction mouvement possible
    elif len(paths) == 2:
        ref_path = paths[0]
        mov_path = paths[1]

        img_ref, _ = load_dicom(ref_path)

        # Correction atténuation sur ref
        if apply_attenuation:
            img_ref = attenuation_correction(img_ref, config)

        aligned = None
        if apply_motion:
            aligned = register_images(ref_path, mov_path, config)

            if aligned is not None and apply_attenuation:
                aligned = attenuation_correction(aligned, config)

        return img_ref, aligned

    # CAS 3 : plusieurs images → série dynamique
    else:
        ref_path = paths[0]
        img_ref, _ = load_dicom(ref_path)

        if apply_attenuation:
            img_ref = attenuation_correction(img_ref, config)

        aligned_list = []

        # traiter les images suivantes
        for mov_path in paths[1:]:
            aligned = None

            if apply_motion:
                aligned = register_images(ref_path, mov_path, config)

                if aligned is not None and apply_attenuation:
                    aligned = attenuation_correction(aligned, config)

            aligned_list.append(aligned)

        return img_ref, aligned_list
