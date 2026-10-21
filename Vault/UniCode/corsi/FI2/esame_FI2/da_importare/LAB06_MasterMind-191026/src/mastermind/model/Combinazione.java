package mastermind.model;

public class Combinazione {
	
	
	PioloDiGioco[] pioli;
	int dim;

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
	
	public String getPiolo(int i) {
		return this.pioli[i].rgb();
	}
	
	
	
	
	
	

}
