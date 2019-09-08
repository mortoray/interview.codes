class Mutex {
	constructor() {
		this.count = 0
	}

	/**
		Tries to acquire the mutex.
		
		If a lock can be acquired, then `true` is returned, otherwise `false` is returned.
	*/
	tryLock = () => {
		if (this.count == 0) {	
			this.count = 1
			return true
		}
		
		return false
	}
	
	/**
		Releases the mutex.
	*/
	unlock = () => {	
		this.count = 0
	}
}
