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
		
		if(risposta.vittoria()) {
			this.status = Status.VITTORIA;
		} else if (this.tentativiRimasti() == 0) {
			this.status = Status.PERSO;
		} else this.status = Status.IN_CORSO;
		
		return this.status;
	}
	
	public Combinazione ultimoTentativo() {
		if(this.tentativiEffettuati() == 0) {
			return null;
		}
		return tentativi[this.tentativiEffettuati()-1];
	}
	
	public Risposta ultimaRisposta() {
		if(this.tentativiEffettuati() == 0) {
			return null;
		}
		return risposte[this.tentativiEffettuati()-1];
	}
	
	public Combinazione tentativo(int i) {
		return tentativi[i];
	}
	
	public Risposta risposta(int i) {
		return risposte[i];
	}
	
	public String situazione() {
		StringBuilder sb = new StringBuilder();
		sb.append(this.tentativiEffettuati() + 1);
		sb.append(")");
		sb.append(" " + this.tentativi[this.tentativiEffettuati()].toString());
		sb.append("\t\t");
		sb.append(this.risposte[this.tentativiEffettuati()].toString());
		sb.append(System.lineSeparator());
		
		return sb.toString();
	}
	
	
	
	
	
	
	
	
	

}
