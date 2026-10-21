package mastermind.model;

public class Combinazione {
	
	
	PioloDiGioco[] pioli;
	int dim;

	public Combinazione(PioloDiGioco[] pioli) {
		super();
		for (int i = 0; i < this.dim; i++) {
			this.pioli[i] = null;
		}
		
	}
	
	public int dim() {
		return pioli.length;
	}
	
	
	
	
	

}
