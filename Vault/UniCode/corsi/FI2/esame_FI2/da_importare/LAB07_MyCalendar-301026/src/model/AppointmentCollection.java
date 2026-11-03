package model;

public class AppointmentCollection {

	private static final int DEFAULT_GROWTH_FACTOR = 2;
	private static final int DEFAULT_PHYSICAL_SIZE = 10;
		
	private Appointment[] innerContainer;
	private int size;
	
	public AppointmentCollection(int capacity) {
		innerContainer = new Appointment[capacity];
		size = 0;
	}
	
	public AppointmentCollection() {
		this(DEFAULT_PHYSICAL_SIZE); //rimando a un altro costruttore con this()
	}
	
	
	public void add(Appointment appointment) {
		if (innerContainer.length == size) {
			AppointmentCollection app = new AppointmentCollection(this.innerContainer.length + this.DEFAULT_GROWTH_FACTOR);
			for(int i = 0; i < size; i++) {
				app[i] = appointment[i];
			}
		}else {
			this.innerContainer[size] = appointment;
		}
	}
	
	
	
	
	
	
	
	
}
