package mastermind.model;

import java.util.StringJoiner;

public class Combinazione {
	
	
	private PioloDiGioco[] pioli;
	private int dim;

	public Combinazione(int dim) {
		super();
		this.pioli = new PioloDiGioco[dim];
		this.dim = dim;
		for (int i = 0; i < this.dim; i++) {
			this.pioli[i] = PioloDiGioco.VUOTO;
		}
		
	}
	
	public int dim() {
		return pioli.length;
	}
	
	public PioloDiGioco getPiolo(int i) {
		return this.pioli[i];
	}
	
	public void setPiolo(int i, PioloDiGioco colore) {
		this.pioli[i] = colore;
	}
	
	public boolean equals(Combinazione c2) {
		
		if(c2 == null) {
			return false;
		}
		
		if(this.dim() == c2.dim()) {
			for(int i=0; i<this.dim(); i++) {
				if (this.pioli[i] != c2.pioli[i]) {
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
