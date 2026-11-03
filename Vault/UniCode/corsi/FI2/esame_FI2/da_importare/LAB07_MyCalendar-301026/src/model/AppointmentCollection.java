package model;

public class AppointmentCollection {

	private static final int DEFAULTH_GROWTH_FACTOR = 2;
	private static final int DEFAULT_PHYSICAL_SIZE = 10;
		
	private Appointment[] innerContainer;
	private int size;
	
	public AppointmentCollection(int dim) {
		this.size = dim;
		new AppointmentCollection(this.size);
	}
	
	public AppointmentCollection() {
		this(DEFAULT_PHYSICAL_SIZE);
	}
	
	
	
	
	
	
	
	
	
}
