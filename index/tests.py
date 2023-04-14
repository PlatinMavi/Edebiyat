from django.test import TestCase

# Create your tests here.

from django.test import TestCase
from index.models import Comment,Creator,LiteratureObject,Vote,VoteableObject

class AnimalTestCase(TestCase):
	def setUp(self):
		self.assertTrue(True,"test haha")

	def test_animals_can_speak(self):
		"""Animals that can speak are correctly identified"""
		self.assertTrue(True,"test2 haha")