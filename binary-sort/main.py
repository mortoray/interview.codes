from typing import *
from typing_extensions import Protocol #type: ignore
import abc


"""
	Declare a type that is comparable with less-than. Less-than is all that is used for most sorting in Python and other languages.
"""
class Comparable(Protocol):
	@abc.abstractmethod
	def __lt__(self, other: Any) -> bool:
		return False
		
ComparableT = TypeVar('ComparableT', bound = Comparable)


"""
	Search for a given value in a list of values. This assumes the input values are sorted and Comparable.
	
	This version has an issue in the case of duplicates. It can't provide any guarantee which one will be found. See `alt_binary_search`
"""
def binary_search( value : ComparableT, items : Sequence[ComparableT] ) -> Optional[int]:
	lo = 0
	hi = len(items)
	
	while lo < hi:
		mid = (hi - lo) // 2 + lo
		
		if items[mid] < value:
			# continue in right side
			lo = mid + 1
		
		elif value < items[mid]:
			# continue in left side
			hi = mid - 1
		
		else:
			return mid
	
	return None
	
	

"""
	Find the lower-bound of a value in the list. This is the first position where the item in the list is not less 
	than the value.
	
	The standard Python library has a comparable function: bisect.bisect_left
"""
def lower_bound( value : ComparableT, items : Sequence[ComparableT] ) -> int:
	lo = 0
	hi = len(items)
	
	while lo < hi:
		mid = (hi - lo) // 2 + lo
		
		if items[mid] < value:
			# continue in right side, add one, as the lower_bound is strictly after `mid`
			lo = mid + 1
		
		else:
			# continue in left side, don't subtract one as the lower_bound may still be `mid`
			hi = mid
	
	return lo
	
	
"""
	Find the upper-bound of a value in the list. This is the first position in where the item is greater than the
	value. 
	
	Note: The algorithm is expressed only in terms of less-than, as that is all that our Comparable is required to support.
"""
def upper_bound( value : ComparableT, items : Sequence[ComparableT] ) -> int:
	lo = 0
	hi = len(items)
	
	while lo < hi:
		mid = (hi - lo) // 2 + lo
		
		if value < items[mid]:
			# continue in left side, don't add one, since the upper_bound may still be `mid`
			hi = mid
		
		else:
			# continue in rights side, add one since the lower_bound is strictly after `mid`
			lo = mid + 1
	
	return lo

	
"""
	An alternate form of binary_search that uses lower_bound.
	
	This version guarantees, that in the case of duplicates, the first one in the list will be returned. These types of guarantees are often sought in algorithms, to ensure code always performs the same. You don't want ambiguous APIs.
"""
def alt_binary_search( value : ComparableT, items : Sequence[ComparableT] ) -> Optional[int]:
	lower = lower_bound( value, items )
	
	if lower >= len( items ):
		return None
		
	if items[lower] < value:
		return None
		
	if value < items[lower]:
		return None
		
	return lower
	

def test_run() -> None:
	items = [ 'a', 'a', 'b', 'f', 'g', 'i', 'r', 't', 'u', 'u', 'x', 'z' ]
	
	assert binary_search( 'g', items ) == 4
	assert binary_search( 'q', items ) == None
	assert binary_search( 'z', items ) == 11
	assert binary_search( 'r', items ) == 6
	assert binary_search( 'y', items ) == None
	# For duplicates our algorithm provides no guarantee which one is returned
	assert binary_search( 'a', items ) in [0,1]
	assert binary_search( 'u', items ) in [8,9]
	
	assert lower_bound( 'a', items ) == 0
	assert lower_bound( 'u', items ) == 8
	assert lower_bound( 'c', items ) == 3
	assert lower_bound( 'y', items ) == 11
	assert lower_bound( 'zz', items ) == 12
	
	assert upper_bound( 'a', items ) == 2
	assert upper_bound( 'u', items ) == 10
	assert upper_bound( 'c', items ) == 3
	assert upper_bound( 'y', items ) == 11
	assert upper_bound( 'zz', items ) == 12
	
	assert alt_binary_search( 'g', items ) == 4
	assert alt_binary_search( 'q', items ) == None
	assert alt_binary_search( 'z', items ) == 11
	assert alt_binary_search( 'r', items ) == 6
	assert alt_binary_search( 'y', items ) == None
	# Search result of 'a' and 'u' is now defined to be the first one in the list
	assert alt_binary_search( 'a', items ) == 0
	assert alt_binary_search( 'u', items ) == 8
	
test_run()
