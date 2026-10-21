package mastermind.model;

import java.util.StringJoiner;

public class Risposta {
	
	private PioloRisposta[] pioli;
	private int dim;

	public Risposta(int dim) {
		super();
		this.pioli = new PioloRisposta[dim];
		this.dim = dim;
		for (int i = 0; i < this.dim; i++) {
			this.pioli[i] = PioloRisposta.VUOTO;
		}
		
	}
	
	public int dim() {
		return pioli.length;
	}
	
	public PioloRisposta getPiolo(int i) {
		return this.pioli[i];
	}
	
	public void setPiolo(int i, PioloRisposta colore) {
		this.pioli[i] = colore;
	}
	
	public boolean equals(Risposta c2) {
		
		if(c2 == null) {
			return false;
		}
		
		if(this.dim() == c2.dim()) {
			for(int i=0; i<this.dim(); i++) {
				if (this.pioli[i] != c2.getPiolo(i)) {
					return false;
				}
			}
			return true;
		}
		return false;
	}
	
	
	public String toString() {
		StringJoiner sj = new StringJoiner(",");
		for (int i = 0; i < this.dim(); i++) {
			sj.add(this.pioli[i].toString());
		}
		return sj.toString();
	}
	

}
