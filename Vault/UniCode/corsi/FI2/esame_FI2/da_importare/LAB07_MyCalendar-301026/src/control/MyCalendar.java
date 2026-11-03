package control;

import model.AppointmentCollection;
import model.Appointment;          // servirà subito anche questa, per add e remove

public class MyCalendar {

	private AppointmentCollection allAppointments;

	public MyCalendar() {
		super();
		this.allAppointments = new AppointmentCollection();
	}
	
	public void add(Appointment app) {
		allAppointments.add(app);
	}
	
	public AppointmentCollection getAllAppointments() {
		return allAppointments;
	}
	
	public boolean remove (Appointment app) {
		return allAppointments.remove(allAppointments.indexOf(app));
	}

	
}
