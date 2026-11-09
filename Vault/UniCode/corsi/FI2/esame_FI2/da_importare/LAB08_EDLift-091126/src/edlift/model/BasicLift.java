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
			return RequestResult.ACCEPTED;
		} else if (this.getCurrentFloor() > this.getRequestedFloor()) {
			BasicLift.super.setCurrentState(LiftState.DOWN);
			return RequestResult.ACCEPTED;
		} else return RequestResult.REJECTED;
	}
}
