package edlift.model;

public class HealthyLift extends Lift {

	public HealthyLift(int minFloor, int maxFloor, int initialFloor, double speed) {
		super(minFloor, maxFloor, initialFloor, speed);
		// TODO Auto-generated constructor stub
	} 
	
	@Override
	public String getMode() {
		return "HEALTHY";
	}
	
	@Override
	public RequestResult goToFloor(int floor) {
		checkArrivalFloor(floor);
		if (getCurrentState() != LiftState.REST ||
				getCurrentFloor() - floor == 1 || 
				getCurrentFloor() - floor == -1 ) {
			return RequestResult.REJECTED;
		}
		
		if (getCurrentFloor() > floor) {
			setRequestedFloor(floor + 1);
			RequestResult.MODIFIED.setFloor(floor+1);
			RequestResult.MODIFIED.setMsg("modified from " + floor + " to " + getRequestedFloor());
			return RequestResult.MODIFIED;
		} else {
			setRequestedFloor(floor - 1);
			RequestResult.MODIFIED.setFloor(floor-1);
			RequestResult.MODIFIED.setMsg("modified from " + floor + " to " + getRequestedFloor());
			return RequestResult.MODIFIED;
		}
	} 
		
}
	


