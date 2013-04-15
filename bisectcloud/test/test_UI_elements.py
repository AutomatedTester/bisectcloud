import test_utils

class UIElements(test_utils.TestCase):

    def test_we_load_home_template_for_root(self):
        response = self.client.get("/en-US/")
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed('templates/home.html', response)
