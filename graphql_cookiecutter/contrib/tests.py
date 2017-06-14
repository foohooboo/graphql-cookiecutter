from django.test import TestCase

class PackageTests(TestCase):

    def setUp(self):
        pass

    def test_imports(self):
        import django
        import pytz
        
        import rest_framework
        
        
        import graphene
        import graphene_django
        