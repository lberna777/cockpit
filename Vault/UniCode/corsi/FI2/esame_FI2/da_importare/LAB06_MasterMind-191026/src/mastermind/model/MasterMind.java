package mastermind.model;

import java.util.Random;

public class MasterMind {
	
	private Combinazione segreta;
	
	public Risposta calcolaRisposta(Combinazione tentativo) {
		//sintetizza e restituisce la Risposta per una Combinazione
		Risposta risposta = new Risposta(segreta.dim());
		int neri = 0, bianchi = 0, totali = 0;
		for(int i = 0; i < tentativo.dim(); i++) {
			
			if(segreta.getPiolo(i).equals(tentativo.getPiolo(i))) {
				neri++;
			}
		}
		int[] occT = occorrenze(tentativo);
		int[] occS = occorrenze(segreta);
		
		for (int j = 0; j < occS.length; j++) {
			totali = totali + Math.min(occT[j], occS[j]);
			//System.out.println("\ntotali = " + totali);
		}
		

		bianchi = totali - neri;
		//System.out.println("\n" + bianchi + " = " + totali + " - " + neri);

		
		for (int y = 0; y < tentativo.dim(); y++) {
			if (neri != 0) {
				risposta.setPiolo(y, PioloRisposta.NERO);
				neri--;
			}
			else if (neri == 0 && bianchi != 0) {
				risposta.setPiolo(y, PioloRisposta.BIANCO);
				bianchi--;
			}
			else if (neri == 0 && bianchi == 0){
				risposta.setPiolo(y, PioloRisposta.VUOTO);
			}
		}
		
		//System.out.print("\nTentativo: " + tentativo.toString() + "\n");
		//System.out.print("\nSegreta: " + segreta.toString() + "\n");

		
		//System.out.println("\nneri = " + neri + ", bianchi = " + bianchi + ", Totali = " + totali);
		
		//System.out.print("\nRisposta: " + risposta.toString() + "\n---");
		
		
		return risposta;	
	}
	
	
	public String combinazioneSegreta() {
		return segreta.toString();
	}

	public MasterMind(int lunghezzaCodice) {	//riceve lunghezza
		super();
		segreta = new Combinazione(lunghezzaCodice); //sorteggia il content
		sorteggiaCombinazione(segreta);
	}
	
	private int[] occorrenze(Combinazione tentativo) {
			//usato da calcolaRisposta, restituisce un array di interi
		//che specifica quante occorrenze per ciascun colore
		int[] occ = new int[PioloDiGioco.values().length]; //7 celle tutte 0
		for(int i = 0; i < tentativo.dim(); i++) {
			PioloDiGioco n = tentativo.getPiolo(i);
			occ[n.ordinal()]++;
		}
		
		return occ;
	}
	
	protected void sorteggiaCombinazione(Combinazione segreta) {
		//popola di colori la combinazione ricevuta come arg
		Random gen = new Random();
		for (int i = 0; i < segreta.dim(); i++) {
			int n = gen.nextInt(PioloDiGioco.values().length - 1) + 1; //6 quindi da 0 a 5 piu uno quindi da 1 a 6
			segreta.setPiolo(i, PioloDiGioco.values()[n]);
				
		}
	}
	
	
	
	

}
