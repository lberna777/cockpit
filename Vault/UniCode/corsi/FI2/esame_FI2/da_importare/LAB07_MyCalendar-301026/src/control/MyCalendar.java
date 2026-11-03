package control;

import model.AppointmentCollection;

import java.time.LocalDateTime;

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
		
		int index = allAppointments.indexOf(app);
		if (index == -1) {
			return false;
		} else {
			allAppointments.remove(index);
			return true;
		}
	}
	
	private AppointmentCollection getAppointmentsIn(LocalDateTime start, LocalDateTime finish) {
	
	AppointmentCollection coll = new AppointmentCollection();
	
	for (int i = 0; i < allAppointments.size(); i++) {
			if (isOverlapped(allAppointments.get(i).getFrom(), allAppointments.get(i).getTo(), start, finish)) {
				coll.add(allAppointments.get(i));
			}
		}
	
	return coll;
	}
	
	private boolean isOverlapped(LocalDateTime start, LocalDateTime finish, LocalDateTime refStart, LocalDateTime refEnd) {
		return finish.isAfter(refStart) && start.isBefore(refEnd);
	}
	
	
	
	
	

	
}
