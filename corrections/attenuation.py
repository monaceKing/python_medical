import numpy as np

def attenuation_correction(image, config):
    """
    Correction d'atténuation simple basée sur un modèle exponentiel.
    Formule utilisée :
        I_corrigée = I_observée x exp(μ x profondeur)

    Paramètres:
    -----------
    image : np.ndarray
        Image scintigraphique brute.
    config : dict
        Paramètres tels que :
        - mu : coefficient d'atténuation
        - depth : profondeur moyenne en cm

    Retour:
    -------
    corrected : np.ndarray
        Image corrigée et normalisée.
    """
 
    # Récupération des paramètres
    mu = config.get("mu", 0.15)       # Coefficient d'atténuation par défaut
    depth = config.get("depth", 12.0) # Profondeur moyenne du patient

    # Facteur correctif basé sur la physique de l'atténuation
    correction_factor = np.exp(mu * depth)

    # Application du facteur
    corrected = image * correction_factor

    # Normalisation à l'échelle scintigraphique (0 – 4095)
    corrected = corrected / corrected.max() * 4095

    return corrected.astype(np.float32)
