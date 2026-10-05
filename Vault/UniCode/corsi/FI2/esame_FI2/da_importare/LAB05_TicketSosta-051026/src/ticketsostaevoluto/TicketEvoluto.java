package ticketsostaevoluto;

import java.text.NumberFormat;
import java.time.Duration;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.time.format.FormatStyle;
import java.util.Locale;

public class TicketEvoluto {
	private double costo;
	private LocalDateTime fine;
	private LocalDateTime inizio;
	
	public TicketEvoluto( LocalDateTime inizio, LocalDateTime fine, double costo) {
		super();
		this.costo = costo;
		this.fine = fine;
		this.inizio = inizio;
	}

	public double getCosto() {
		return costo;
	}

	public LocalDateTime getFine() {
		return fine;
	}

	public LocalDateTime getInizio() {
		return inizio;
	}

	@Override
	public String toString() {
		return "SOSTA AUTORIZZATA---\n" +
				"Dalle " + inizio.format(DateTimeFormatter.ofLocalizedTime(FormatStyle.SHORT).withLocale(Locale.ITALY)) +
				" del giorno " + inizio.format(DateTimeFormatter.ofLocalizedDate(FormatStyle.SHORT).withLocale(Locale.ITALY)) +
				" alle " + fine.format(DateTimeFormatter.ofLocalizedTime(FormatStyle.SHORT).withLocale(Locale.ITALY)) +
				" del giorno " + fine.format(DateTimeFormatter.ofLocalizedDate(FormatStyle.SHORT).withLocale(Locale.ITALY)) +
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