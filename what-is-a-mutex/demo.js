// a single mutex that all threads will use
mutex = new Mutex()

// tracks how many threads have acquired the mutex, it should be 0 or 1 or there is an error
concurrentCount = 0

// simulates a thread that is idle, waiting for the mutex, or has acquired the mutex and running
class Thread {
	constructor( id, mutex ) {
		this.id = id
		this.mutex = mutex
	}
	
	addTo = ( where ) => {
		const threadBlock = `
			<div class="thread" id='thread_${this.id}'>
				<button class='action-button'></button>
				<div class='img'/>
			</div>
			`
			
		this.block = document.createElement( 'div' )
		this.block.innerHTML = threadBlock
		
		where.appendChild( this.block )
		
		this.action = this.block.getElementsByClassName( 'action-button' )[0]
		this.idle()
	}
	
	idle = () => {
		this.block.className = 'idle'
		this.setAction( 'Run', this.run )
	}
	
	setAction = ( label, action ) => {
		this.action.innerHTML = label
		if( action == null ) {
			this.action.disabled = true
		} else {
			this.action.disabled = false
			this.action.onclick = action
		}
	}
	
	run = () => {
		this.setAction( 'Waiting', null )
		this.block.className = 'wait'
		this.interval = setInterval( this.tryRun, 100 )
	}
	
	tryRun = () => {
		if( mutex.tryLock() ) {
			if( concurrentCount != 0 ) {
				alert( "Uh oh, mutliple threads have acquired the mutex at the same time" )
			}
			
			concurrentCount++
			clearInterval( this.interval )
			this.block.className = 'locked'
			this.setAction( 'Unlock', this.unlock )
		}
	}
	
	unlock = () => {
		concurrentCount--
		this.mutex.unlock()
		this.idle()
	}
}

let threadCount = 0
function addThread() {
	let where = document.getElementById( 'threads' )
	let id = threadCount
	threadCount++
	(new Thread(id, mutex)).addTo( where )
}

