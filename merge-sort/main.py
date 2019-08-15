from typing import *
from typing_extensions import Protocol #type: ignore
import abc, random

"""
	Declare a type that is comparable with less-than. Less-than is all that is used for most sorting in Python and other languages.
"""
class Comparable(Protocol):
	@abc.abstractmethod
	def __lt__(self, other: Any) -> bool:
		return False
		
ComparableT = TypeVar('ComparableT', bound = Comparable)


"""
	Sorts a list using the merge sort algorithm.
"""
def merge_sort( items : List[ComparableT] ) -> List[ComparableT]:
	# The trivial cases
	if len( items ) <= 1:
		return items
		
	# Divide
	mid = len(items) // 2
	fore = merge_sort( items[:mid] )
	back = merge_sort( items[mid:] )
	
	# Recombine
	out : List[T] = []
	fore_at = 0
	back_at = 0
	while fore_at < len(fore) or back_at < len(back):
		if back_at != len(back) and (fore_at == len(fore) or back[back_at] < fore[fore_at]):
			out.append( back[back_at] )
			back_at += 1
		else:
			out.append( fore[fore_at] )
			fore_at += 1
			
	return out
	
	
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
	numbers = [random.randint(0,100) for _ in range(20)]
	print( numbers )

	sorted_numbers = merge_sort(numbers)
	verify_sort_result( numbers, sorted_numbers )
	print( sorted_numbers )
	
	
test_run()
