from django.test import TestCase


from ..utils.image_utils import upload_image_or_error


class TestImageUtils(TestCase):

    def setUp(self) -> None:
        self.img_url = "https://www.bhphotovideo.com/images/images2500x2500/focusrite_scarlett_2i2_stu_3g_scarlett_2i2_usb_audio_1479284.jpg"

    def test_upload_image(self):
        pub_id = "Sabigear/Focusrite/Scarlett 2i2/G10/image_1"
        upload = upload_image_or_error(self.img_url, pub_id)

        self.assertEqual(upload.get("public_id"), pub_id)