package model;

import java.time.Duration;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.time.format.FormatStyle;
import java.util.Locale;

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
		setDuration(duration);
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
		this.to = from.plus(duration);
	}

	public boolean equals(Appointment app) {
		
		return (app.description.equals(this.description) && app.from.isEqual(this.from) && app.to.isEqual(this.to));
			
	}

	@Override
	public String toString() {
		return "Appointment: " + description + "\nDA: " + from.format(DateTimeFormatter.ofLocalizedDateTime(FormatStyle.SHORT).withLocale(Locale.ITALY)) 
		+ "\nA:" + to.format(DateTimeFormatter.ofLocalizedDateTime(FormatStyle.SHORT).withLocale(Locale.ITALY)) + "\nDURATA: " + getDuration();
	}
}
