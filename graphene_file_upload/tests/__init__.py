import unittest

def fun(x):
    return x + 1

class TestDjangoFileUploadGraphQLView(unittest.TestCase):
    def test(self):
        self.assertEqual(fun(3), 4)

class TestFlaskFileUploadGraphQLView(unittest.TestCase):
    def test(self):
        self.assertEqual(fun(3), 4)
