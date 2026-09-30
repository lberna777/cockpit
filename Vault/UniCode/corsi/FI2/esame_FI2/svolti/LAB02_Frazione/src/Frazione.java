import java.util.Objects;


public class Frazione {

	private int num, den;

	public Frazione(int num, int den) {
		super();
		int i = num * den;
		if (i >= 0) {
		this.num = Math.abs(num);
		this.den = Math.abs(den);
		} else if (i < 0) {
			this.num = -Math.abs(num);
			this.den = Math.abs(den);
		}
	}
	
	public Frazione(int num) {	
		this(num, 1);	
	}
	
	// Grazie al costruttore ausiliario, le frazioni che esprimono
	// valori interi si possono esprimere più efficacemente:
	//	f8 = new Frazione(8);

	// Una volta che i valori sono “dentro” l’entità, occorre poterli
	// “vedere” da fuori, implemento due ACCESSOR pubblici get
	
	
	public int getNum() {
		return num;
	}

	public int getDen() {
		return den;
	}

	// NON servono invece i metodi set* perché Frazione è un
	// oggetto immutabile e quindi non può essere cambiato
	// dall’esterno
	
	
	public boolean equals(Frazione f) {
		if ((this.num * f.den) == (this.den * f.num)) {
			return true;
		}else return false;
	}

	@Override
	public String toString() {
		return this.num + "/" + this.den;
	}
	
	
	public Frazione minTerm() {
		if (this.num == 0) {
			return new Frazione(0);
		}
		int divCom = MyMath.mcd((Math.abs(this.num)), Math.abs(this.den));
		return new Frazione(this.num / divCom, this.den / divCom);
	}
	
	
	
	

	
	
	
	
	
	
	
	
}
