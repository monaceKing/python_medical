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

    # Convertir en float32 pour la registration
    fixed = sitk.Cast(fixed, sitk.sitkFloat32)
    moving = sitk.Cast(moving, sitk.sitkFloat32)

    # NOUVEAU : Vérifier et afficher les dimensions
    print(f"Fixed image size: {fixed.GetSize()}")
    print(f"Moving image size: {moving.GetSize()}")
    print(f"Fixed image dimension: {fixed.GetDimension()}")
    print(f"Moving image dimension: {moving.GetDimension()}")

    # CORRECTION : Si les images sont 3D, extraire une slice 2D
    if fixed.GetDimension() == 3:
        fixed = fixed[:, :, 0]  # Prendre la première slice
    if moving.GetDimension() == 3:
        moving = moving[:, :, 0]

    # CORRECTION : Redimensionner moving si tailles différentes
    if fixed.GetSize() != moving.GetSize():
        print("Resizing moving image to match fixed image...")
        moving = sitk.Resample(
            moving, fixed,
            sitk.Transform(),
            sitk.sitkLinear,
            0.0,
            moving.GetPixelID()
        )

    # Définition de la transformation rigide
    transform = sitk.Euler2DTransform()

    # Configuration de la méthode d'enregistrement
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

    # Application de la transformation obtenue à l'image déplacée
    aligned = sitk.Resample(
        moving, fixed, final_transform,
        sitk.sitkLinear, 0.0,
        moving.GetPixelID()
    )

    # Conversion SimpleITK → NumPy
    aligned_numpy = sitk.GetArrayFromImage(aligned).astype(np.float32)

    return aligned_numpy