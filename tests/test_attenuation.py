from corrections.attenuation import attenuation_correction
import numpy as np

def test_attenuation_output_shape():
    img = np.ones((128,128), dtype=np.float32)
    config = {"mu": 0.15, "depth": 10}
    out = attenuation_correction(img, config)
    assert out.shape == img.shape
