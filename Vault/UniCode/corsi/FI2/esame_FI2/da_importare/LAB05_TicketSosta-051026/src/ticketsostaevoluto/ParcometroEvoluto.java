package ticketsostaevoluto;

import java.time.Duration;
import java.time.LocalDate;
import java.time.LocalDateTime;
import java.time.LocalTime;
import ticketsosta.Tariffa;

public class ParcometroEvoluto {

	private Tariffa[] tariffa;

	public ParcometroEvoluto(Tariffa[] tariffa) {
		super();
		this.tariffa = tariffa;
	}
	
	private double calcolaCosto(double costoOrario, LocalTime da, LocalTime a) {
		Duration durataSosta;
		if (a.isBefore(da) || LocalTime.of(0, 0).equals(a)) {
			durataSosta = Duration.between(da, LocalTime.of(23, 59)).plusMinutes(1);   // fino a fine giornata
		} else {
			durataSosta = Duration.between(da, a);                                     // caso normale
		}
		return costoOrario * durataSosta.toMinutes() / 60.0;   // minuti → ore, poi × tariffa
	}
	
	private double calcolaCostoSuPiuGiorni(LocalDateTime da, LocalDateTime a) {
		double res = 0;
		LocalDate giorno = da.plusDays(1).toLocalDate();	
		
		if (da.toLocalDate().equals(a.toLocalDate())) {
			Tariffa t = tariffa[da.getDayOfWeek().getValue() - 1];                  // la tariffa del giorno
			LocalDateTime daEffettivo = da.plusMinutes(t.getMinutiFranchigia());    // l'inizio dopo i minuti gratis
			long minutiDaPagare = Duration.between(daEffettivo, a).toMinutes();     // minuti rimasti da pagare
			if (minutiDaPagare < t.getDurataMinima()) {                             // meno del minimo?
				return t.getTariffaOraria() * t.getDurataMinima() / 60.0;           // paghi il minimo
			}
			return calcolaCosto(t.getTariffaOraria(), daEffettivo.toLocalTime(), a.toLocalTime());   // altrimenti come prima
		}
		
		res = calcolaCosto(tariffa[da.getDayOfWeek().getValue() - 1].getTariffaOraria(), da.plusMinutes(tariffa[da.getDayOfWeek().getValue() - 1].getMinutiFranchigia()).toLocalTime(), LocalTime.MIDNIGHT  );
		while(giorno.isBefore(a.toLocalDate())){
			res = res + calcolaCosto(tariffa[giorno.getDayOfWeek().getValue() - 1].getTariffaOraria(), LocalTime.MIDNIGHT, LocalTime.MIDNIGHT  );
			giorno = giorno.plusDays(1);
		}
		return res = res + calcolaCosto(tariffa[a.getDayOfWeek().getValue() - 1].getTariffaOraria(), LocalTime.MIDNIGHT, a.toLocalTime());
		
	}
	
	public TicketEvoluto emettiTicket(LocalDateTime inizio, LocalDateTime fine) {
		return new TicketEvoluto(inizio, fine, calcolaCostoSuPiuGiorni(inizio, fine));
	}

	@Override
	public String toString() {
		String s = "Parcometro configurato con le tariffe:\n";      // l'intestazione
		for (int i = 0; i < 7; i++) {
			s = s + tariffa[i].toString() + "\n";        // una tariffa per riga
		}
		return s;                                                    // restituisci, non stampare
	}
	

}
