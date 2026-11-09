package edlift.model;

public class BasicLift extends Lift{

	public BasicLift(int minFloor, int maxFloor, int initialFloor, double speed) {
		super(minFloor, maxFloor, initialFloor, speed);
	}

	public String getMode() {
		return "BASIC LIFT";
	}
	
	
	public RequestResult goToFloor(int floor) {
		if (BasicLift.super.getCurrentState() != LiftState.REST) {
			return RequestResult.REJECTED;
		}
		
		BasicLift.super.setRequestedFloor(floor);
		if(this.getCurrentFloor() < this.getRequestedFloor()) {
			BasicLift.super.setCurrentState(LiftState.UP);
		} else if (this.getCurrentFloor() > this.getRequestedFloor()) {
			BasicLift.super.setCurrentState(LiftState.DOWN);
		} else return RequestResult.REJECTED;
		
		this.setCurrentFloor(this.getRequestedFloor());
		this.setCurrentState(LiftState.REST);
		
	}
}
