package edlift.model;

public class BasicLift extends Lift{

	public BasicLift(int minFloor, int maxFloor, int initialFloor, double speed) {
		super(minFloor, maxFloor, initialFloor, speed);
	}

	@Override
	public String getMode() {
		return "BASIC";
	}
	
	@Override
	public RequestResult goToFloor(int floor) {
		
		checkArrivalFloor(floor);
		if (getCurrentState() != LiftState.REST) {
			return RequestResult.REJECTED;
		}
		
		setRequestedFloor(floor);
		return RequestResult.ACCEPTED;
	} 
}
