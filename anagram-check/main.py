from typing import  *
import unicodedata

# Unfortunately grapheme clusters are not part of the standard Python library yet
# This library refers to grapheme cluster groups as graphemes
import grapheme


"""
	Checks if two words are anagrams of each other.
"""
def are_anagrams( a : str, b : str ) -> bool:
	# Convert sequences/chars to a common representation
	def convert( a : str ) -> str:
		return a.lower()
		
	# Filter out pieces we don't care about
	def filter( a : str ) -> bool:
		if a.isspace():
			return False
		return True
		
	def to_sort_list( q : str ):
		return sorted([convert(c) for c in q if filter(c)])
		
	list_a = to_sort_list(a)
	list_b = to_sort_list(b)
	return list_a == list_b

	
"""
	Checks if two words are anagrams of each other with consideration of Unicode grapheme clusters.
"""
def are_anagrams_unicode( a : str, b : str ) -> bool:
	# Convert sequences/chars to a common representation
	def convert( a : str ) -> str:
		return a.lower()
		
	# Filter out pieces we don't care about
	def filter( a : str ) -> bool:
		if a.isspace():
			return False
		return True
		
	def to_sort_list( q : str ):
		q = unicodedata.normalize('NFKD', q) #compatible decomposed form
		gc = grapheme.graphemes(q)
		return sorted([convert(c) for c in gc if filter(c)])
		
	list_a = to_sort_list(a)
	list_b = to_sort_list(b)
	return list_a == list_b

	
"""
	Checks if two words are anagrams of each other with consideration of the root (first) code in the
	Unicode grapheme clusters.
"""
def are_anagrams_base( a : str, b : str ) -> bool:
	# Convert sequences/chars to a common representation
	def convert( a : str ) -> str:
		# assume first element is the logical base character in decomposed form
		return a[0].lower()
		
	# Filter out pieces we don't care about
	def filter( a : str ) -> bool:
		if a.isspace():
			return False
		return True
		
	def to_sort_list( q : str ):
		q = unicodedata.normalize('NFKD', q) #compatible decomposed form
		gc = grapheme.graphemes(q)
		return sorted([convert(c) for c in gc if filter(c)])
		
	list_a = to_sort_list(a)
	list_b = to_sort_list(b)
	return list_a == list_b
	

def test_main():
	assert are_anagrams( "proteins", "pointers" )
	
	# ignores case
	assert are_anagrams( "Eats", "Seat" )
	
	# ignores spaces
	assert are_anagrams( "I like Python", "The Pinky Oil" )
	
	# negatives
	assert not are_anagrams( "AAAbb", "aaab" )

	
def test_unicode():
	fr_a = "trêve"
	fr_b = "reve\u0302t"
	# Won't work since the composition is different for the ê
	assert not are_anagrams( fr_a, fr_b )
	
	assert are_anagrams_unicode( fr_a, fr_b )
	
	# These are not anagrams as the combining character is elsewhere -- requires the grapheme clusters to work correctly
	assert not are_anagrams_unicode( "äe", "aë" )
	
	# What if you wanted this to be equivalent (accent equivalency)
	fr_c = "verte"
	assert not are_anagrams_unicode( fr_a, fr_c )
	assert are_anagrams_base( fr_a, fr_c )
	assert are_anagrams_base( "noël", "Léon" )
	

def test_emoji():
	assert are_anagrams( "☺️☹️", "☺️☹️" )
	assert are_anagrams_unicode( "☺️☹️", "☺️☹️" )
	assert are_anagrams_base( "☺️☹️", "☺️☹️" )

	assert not are_anagrams_base( "☺️", "☹️" )
	
	# The base test should also work for colored emoji, it'll take the base emoji, dropping the color
	# Refer to http://www.unicode.org/reports/tr51/
	light_hand = "👍\U0001F3FB"
	dark_hand = "👍\U0001F3FF"
	assert not are_anagrams_unicode( light_hand, dark_hand )
	assert are_anagrams_base( light_hand, dark_hand )


test_emoji()
