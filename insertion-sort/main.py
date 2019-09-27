from typing import *
from typing_extensions import Protocol #type: ignore
import abc

import bisect, random, string


"""
	Declare a type that is comparable with less-than. Less-than is all that is used for most sorting in Python and other languages.
"""
class Comparable(Protocol):
	@abc.abstractmethod
	def __lt__(self, other: Any) -> bool:
		return False
		
ComparableT = TypeVar('ComparableT', bound = Comparable)


"""
	Insert a value into a sorted list.
"""
def insert_into_sorted( value : ComparableT, items : List[ComparableT] ) -> None:
	where = upper_bound( value, items )
	items.insert( where, value )
	
	
"""
	Sorts a list using insertion sort.
"""
def insertion_sort( items : List[ComparableT] ) -> List[ComparableT]:
	out : List[ComparableT] = []
	for item in items:
		insert_into_sorted( item, out )
		
	return out
	
	
"""
	Find the upper-bound of a value in the list. This is the first position in where the item is greater than the
	value. 
	
	Refer to the [Binary Search](https://skl.sh/2mfgk4W) class for how to write an upper-bound function.
"""
def upper_bound( value : ComparableT, items : Sequence[ComparableT] ) -> int:
	return bisect.bisect_right( items, value )


"""
	Checks the validty of the sorting result.
"""
def verify_sort_result( original : List[ComparableT], result : List[ComparableT] ) -> None:
	# Check that all the original items are in the result, and nothing more
	dup_result = result[:]
	for item in original:
		dup_result.remove(item)
	assert len(dup_result) == 0
	
	# Ensure a valid ordering
	for i in range(len(result)-1):
		assert not (result[i+1] < result[i])

		

def test_run() -> None:
	letters = [random.choice(string.ascii_uppercase) for _ in range(20)]
	print( letters )
	
	sorted_letters = insertion_sort( letters )
	verify_sort_result( letters, sorted_letters )
	print( sorted_letters )

	
_counted_letters = {}
"""
	Tracks a letter with the count of how often it's been used.
	On comparison only the letter is used and the count ignored.
"""
class CountedLetter():
	def __init__( self, letter ):
		count = _counted_letters.get( letter, 0 )
		_counted_letters[letter] = count + 1
		
		self.value = letter
		self.count = count
		
	def __lt__( self, b : 'CountedLetter' ) -> bool:
		# Ignore the count
		return self.value < b.value
		
	def __str__( self ) -> str:
		return f'{self.value}-{self.count}'

		
"""
	Tests whether insertion_sort is a stable sort.
"""
def test_stable_run() -> None:
	letters = [CountedLetter(random.choice(string.ascii_uppercase)) for _ in range(20)]
	print( [str(s) for s in letters] )
	
	sorted_letters = insertion_sort( letters )
	verify_sort_result( letters, sorted_letters )
	print( [str(s) for s in sorted_letters] )
	
	
test_run()
test_stable_run()
