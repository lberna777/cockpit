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
			AppointmentCollection app = new AppointmentCollection(this.innerContainer.length * this.DEFAULT_GROWTH_FACTOR);
			for(int i = 0; i < size; i++) {
				app.innerContainer[i] = this.innerContainer[i];
			}
			this.innerContainer = app.innerContainer;
		}
			this.innerContainer[size] = appointment;
			size++;
		
	}
	
	
	public Appointment get(int index) {
		return this.innerContainer[index];
	}
	
	public int indexOf(Appointment app) {
		for(int i = 0; i < this.size; i++) {
			if(this.innerContainer[i].equals(app)) {
				return i;
			}
		}
		return -1; 
	}
	
	public int size() {
		return this.size;
	}
	
	public void remove (int index) {
		for(int i = index; i < this.innerContainer.length; i++) {
			this.innerContainer[i] = this.innerContainer[i+1];
		}
		this.innerContainer[innerContainer.length] = null;
		size--;
	}
	
	
	
	
}
	
	
	
	
	
	
	
	
	

