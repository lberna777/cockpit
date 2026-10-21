package mastermind.model;

public class Gioco {
	
	private int maxTentativi;
	private int dim;
	private int numTentativi;
	private Combinazione[] tentativi;
	private Risposta[] risposte;
	private Status status;
	
	
	
	
	
	public Gioco(int maxTentativi, int dim) {
		super();
		this.maxTentativi = maxTentativi;
		this.dim = dim;
		this.numTentativi = 0;
		this.tentativi = new Combinazione[maxTentativi];
		this.risposte = new Risposta[maxTentativi];
		this.status = Status.IN_CORSO;
	}

	public int maxTentativi() {
		return maxTentativi;
	}
	
	public int dimensione() {
		return dim;
	}
	
	public int tentativiEffettuati() {
		return numTentativi;
	}
	
	public int tentativiRimasti() {
		return this.maxTentativi - this.numTentativi;
	}
	
	public Status stato() {
		return status;
	}
	
	public Status registraMossa(Combinazione tentativo, Risposta risposta){
		
		tentativi[this.tentativiEffettuati()] = tentativo;
		risposte[this.tentativiEffettuati()] = risposta;
		
		numTentativi++;
		
		if(risposta.vittoria() == true) {
			return Status.VITTORIA;
		} else if (this.tentativiRimasti() == 0) {
			return Status.PERSO;
		} else return Status.IN_CORSO;
		
		
	}
	
	public Combinazione ultimoTentativo() {
		return tentativi[this.tentativiEffettuati()];
	}
	
	public Risposta ultimaRisposta() {
		return risposte[this.tentativiEffettuati()];
	}
	
	
	
	
	
	
	
	
	

}
