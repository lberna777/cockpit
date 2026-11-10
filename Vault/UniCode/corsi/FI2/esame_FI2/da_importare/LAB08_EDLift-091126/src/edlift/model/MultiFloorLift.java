package edlift.model;
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

	@Override
	public RequestResult goToFloor(int floor) {
		// TODO Auto-generated method stub
		return null;
	}

}
