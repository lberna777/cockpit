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
				floor - getCurrentFloor() == 1 || 
				floor - getCurrentFloor() == -1 ) {
			return RequestResult.REJECTED;
		}
		
		setRequestedFloor(floor - 1);
		return RequestResult.ACCEPTED;
	} 
		
}
	


