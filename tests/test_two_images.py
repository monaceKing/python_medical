from pipeline import process_image
from config import config
import numpy as np

def test_two_images():
    """
    Test du pipeline pour deux images (correction possible du mouvement).
    """
    fake_image1 = np.ones((128,128), dtype=np.float32)
    fake_image2 = np.ones((128,128), dtype=np.float32) * 2
    
    # Override load_dicom
    import utils.dicom_loader as loader
    loader.load_dicom = lambda path: (fake_image1 if "1" in path else fake_image2, None)

    # Override movement correction
    import corrections.movement as move
    move.register_images = lambda a,b,c: fake_image1

    ref_corr, mov_corr = process_image(
        paths=["img1.dcm", "img2.dcm"],
        apply_attenuation=True,
        apply_motion=True,
        config=config
    )

    assert ref_corr is not None
    assert mov_corr is not None
    assert mov_corr.shape == fake_image1.shape
