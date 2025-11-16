import pydicom
import numpy as np

def load_dicom(path):
    """
    Charge une image DICOM scintigraphique.

    Paramètres:
    -----------
    path : str
        Chemin vers le fichier DICOM.

    Retour:
    -------
    image : np.ndarray
        Matrice de l'image.
    metadata : pydicom.dataset.FileDataset
        Métadonnées DICOM complètes.
    """

    # Lecture du fichier DICOM
    ds = pydicom.dcmread(path)

    # Conversion en matrice NumPy en float32 pour le traitement
    image = ds.pixel_array.astype(np.float32)

    return image, ds
