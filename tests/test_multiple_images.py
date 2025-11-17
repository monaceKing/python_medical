from pipeline import process_image
from config import config
import numpy as np

def test_multiple_images():
    """
    Test pour plusieurs images (série dynamique).
    """
    fake_image = np.ones((64, 64), dtype=np.float32)

    # Override loader
    import utils.dicom_loader as loader
    loader.load_dicom = lambda path: (fake_image, None)

    # Override movement
    import corrections.movement as move
    move.register_images = lambda a,b,c: fake_image

    ref_corr, aligned_list = process_image(
        paths=["img1.dcm", "img2.dcm", "img3.dcm"],
        apply_attenuation=True,
        apply_motion=True,
        config=config
    )

    assert isinstance(aligned_list, list)
    assert len(aligned_list) == 2
