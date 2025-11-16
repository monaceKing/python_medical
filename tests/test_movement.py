def test_registration_import():
    from corrections.movement import register_images
    assert callable(register_images)
