package ticketsosta;

import java.text.NumberFormat;
import java.time.Duration;
import java.time.LocalTime;
import java.time.format.DateTimeFormatter;
import java.time.format.FormatStyle;
import java.util.Locale;

public class Ticket {
	private double costo;
	private LocalTime fine;
	private LocalTime inizio;
	
	public Ticket( LocalTime inizio, LocalTime fine, double costo) {
		super();
		this.costo = costo;
		this.fine = fine;
		this.inizio = inizio;
	}

	public double getCosto() {
		return costo;
	}

	public LocalTime getFine() {
		return fine;
	}

	public LocalTime getInizio() {
		return inizio;
	}

	@Override
	public String toString() {
		return "SOSTA AUTORIZZATA---\n" +
				"Dalle " + inizio.format(DateTimeFormatter.ofLocalizedTime(FormatStyle.SHORT).withLocale(Locale.ITALY)) +
				" Alle " + fine.format(DateTimeFormatter.ofLocalizedTime(FormatStyle.SHORT).withLocale(Locale.ITALY)) +
				"\n" + 
				"Durata totale: " + toStringDuration(Duration.between(inizio, fine)) +
				"\n" +
				"Totale pagato: " + getCostoAsString();
	}
	
	public String getCostoAsString() {
		NumberFormat formatter = NumberFormat.getCurrencyInstance(Locale.ITALY);
		return formatter.format(costo);
	}
	
	private String toStringDuration(Duration duration) {
		long dh = duration.toHours();
		long dm = duration.toMinutesPart();
		
		if (dm < 10) {
			return dh + ":" + "0" + dm;
		} else return dh + ":" + dm;		
	}
	
	
	
}
