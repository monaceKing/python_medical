import SimpleITK as sitk
import numpy as np

def register_images(ref_path, mov_path, config):
    """
    Correction du mouvement par registration rigide (translation + rotation).

    Paramètres:
    -----------
    ref_path : str
        Chemin vers l'image de référence (fixe).
    mov_path : str
        Chemin vers l'image déplacée (à aligner)
    config : dict
        Paramètres de registration (ex: nombre de bins)

    Retour:
    -------
    aligned_numpy : np.ndarray
        Image alignée au format NumPy.
    """

    # Chargement des images DICOM
    fixed = sitk.ReadImage(ref_path)
    moving = sitk.ReadImage(mov_path)

    # Définition de la transformation rigide
    transform = sitk.Euler2DTransform()

    # Configuration de la méthode d’enregistrement
    registration = sitk.ImageRegistrationMethod()
    registration.SetInitialTransform(transform, inPlace=False)

    # Utilisation de la Mutual Information (robuste en médecine)
    bins = config.get("registration_bins", 50)
    registration.SetMetricAsMattesMutualInformation(bins)

    # Optimiseur (descente de gradient)
    registration.SetOptimizerAsRegularStepGradientDescent(
        learningRate=2.0,
        minStep=1e-4,
        numberOfIterations=200
    )

    # Interpolation linéaire
    registration.SetInterpolator(sitk.sitkLinear)

    # Exécution de la registration
    final_transform = registration.Execute(fixed, moving)

    # Application de la transformation obtenue à l’image déplacée
    aligned = sitk.Resample(
        moving, fixed, final_transform,
        sitk.sitkLinear, 0.0,
        moving.GetPixelID()
    )

    # Conversion SimpleITK → NumPy
    aligned_numpy = sitk.GetArrayFromImage(aligned).astype(np.float32)

    return aligned_numpy
