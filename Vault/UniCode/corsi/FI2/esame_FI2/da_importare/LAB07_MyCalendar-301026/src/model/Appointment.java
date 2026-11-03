package model;

import java.time.Duration;
import java.time.LocalDateTime;

public class Appointment {

	private String description;
	private LocalDateTime from;
	private LocalDateTime to;
	
	public Appointment(String description, LocalDateTime from, LocalDateTime to) {
		super();
		this.description = description;
		this.from = from;
		this.to = to;
	}
	
	public Appointment(String description, LocalDateTime from, Duration duration) {
		super();
		this.description = description;
		this.from = from;
		this.duration = duration;
	}
	
	
	
	
	
	
}
