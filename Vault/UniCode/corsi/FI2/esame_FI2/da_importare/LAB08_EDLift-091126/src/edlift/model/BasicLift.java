package edlift.model;

public class BasicLift extends Lift{

	public BasicLift(int minFloor, int maxFloor, int initialFloor, double speed) {
		super(minFloor, maxFloor, initialFloor, speed);
	}

	public String getMode() {
		return "BASIC LIFT"
	}
	
}
