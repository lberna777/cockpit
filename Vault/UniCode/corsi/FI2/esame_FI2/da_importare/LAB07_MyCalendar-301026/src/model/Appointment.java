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
		this.to = from.plus(duration);
	}

	public String getDescription() {
		return description;
	}

	public void setDescription(String description) {
		this.description = description;
	}

	public LocalDateTime getFrom() {
		return from;
	}

	public void setFrom(LocalDateTime from) {
		this.from = from;
	}

	public LocalDateTime getTo() {
		return to;
	}

	public void setTo(LocalDateTime to) {
		this.to = to;
	}
	
	
	public Duration getDuration() {
		return Duration.between(from, to);
	}
	
	public void setDuration(Duration duration) {
		duration = duration.between(to, from);
	}
	
	
	
	
	
}
