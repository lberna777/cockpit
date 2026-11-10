package edlift.model;
import com.sun.net.httpserver.Request;

import edlift.model.util.Queue;

public class MultiFloorLift extends Lift {

	private Queue queue;
	
	
	public MultiFloorLift(int minFloor, int maxFloor, int initialFloor, double speed) {
		super(minFloor, maxFloor, initialFloor, speed);
		this.queue = new Queue(4);
		// TODO Auto-generated constructor stub
	}

	@Override
	public String getMode() {
		// TODO Auto-generated method stub
		return "MULTIFLOOR";
	}

	
	public boolean hasPendingFloors() {
		return queue.hasItems();
	}
	
	public int nextPendingFloor(LiftState state) {
		return queue.peek();
	}
	
	@Override
	public RequestResult goToFloor(int floor) {

		// fermo? 
			// se no: tento di inserire la richiesta
				// se c'e' spazio -> return RequestResult.ACCEPTED
				
				// se no -> RequestResult.altro.REJECTED con motivazioni, piano Integer.MIN_VALUE
		
			// se si -> Imposto il piano di destinazione e restituisco ACCEPTED
		checkArrivalFloor(floor);
		if (getCurrentState() == LiftState.REST) {
			return RequestResult.ACCEPTED;
		} else {
			
			if(queue.insert(floor) == true) {
				return RequestResult.ACCEPTED;
			} else  {
				
				RequestResult.REJECTED.setFloor(Integer.MIN_VALUE);
				RequestResult.REJECTED.setMsg("REJECTED: Queue's full");
				return RequestResult.REJECTED;
				

			
				
			}
			
			
		}
		
		
		
		
		
		return null;
	}

	
	
}
