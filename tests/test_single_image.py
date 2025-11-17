from pipeline import process_image
from config import config
import numpy as np

def test_single_image():
    """
    Test du pipeline lorsqu'une seule image est fournie.
    Aucune correction de mouvement ne doit être effectuée.
    """
    fake_image = np.ones((128, 128), dtype=np.float32)
    
    # Fake loader override
    import utils.dicom_loader as loader
    loader.load_dicom = lambda path: (fake_image, None)

    img_corr, mov_corr = process_image(
        paths="fake_image.dcm",
        apply_attenuation=True,
        apply_motion=False,
        config=config
    )

    assert mov_corr is None
    assert img_corr.shape == fake_image.shape
