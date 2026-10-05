package ticketsosta;

import java.time.Duration;
import java.time.LocalTime;

public class Parcometro {

	private Tariffa tariffa;

	public Parcometro(Tariffa tariffa) {
		super();
		this.tariffa = tariffa;
	}
	
	private double calcolaCosto(double costoOrario, LocalTime da, LocalTime a) {

		// 1) durata della sosta, in MINUTI (tipo long: Duration.toMinutes() restituisce long)
		long minutiSosta = Duration.between(da, a).toMinutes(); 

		// 2) franchigia: togli i minuti gratuiti
		//    (il valore sta nella Tariffa del campo, non nei parametri)
		long minutiDaPagare = minutiSosta - tariffa.getMinutiFranchigia();

		// 3) durata minima: se i minuti da pagare sono meno del minimo, paghi il minimo
		if (minutiDaPagare < tariffa.getDurataMinima()) {
			minutiDaPagare = tariffa.getDurataMinima();
		}

		// 4) da minuti a ore e costo, attenzione alla divisione intera
		return costoOrario * (minutiDaPagare / 60.0);
	}
	
	public Ticket emettiTicket(LocalTime inizio, LocalTime fine) {
		return new Ticket(inizio, fine, calcolaCosto(tariffa.getTariffaOraria(), inizio, fine));
	}

	@Override
	public String toString() {
		return "Parcometro configurato con la tariffa: " + tariffa.toString();
	}
	
	
	
	
	
	
	
}
