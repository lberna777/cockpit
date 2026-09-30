/**
 * Frazione come tipo di dato astratto (ADT) - Prima Parte
 * 
 * @author Fondamenti di Informatica T-2
 * @version March 2024
 */
public class Frazione {
	private int num, den;

	/**
	 * Costruttore della Frazione
	 * 
	 * @param num
	 *            Numeratore
	 * @param den
	 *            Denominatore
	 */
	public Frazione(int num, int den) {
		boolean negativo = num * den < 0;
		this.num = negativo ? -Math.abs(num) : Math.abs(num);
		this.den = Math.abs(den);
	}

	/**
	 * Costruttore della Frazione
	 * 
	 * @param num
	 *            Numeratore
	 */
	public Frazione(int num) {
		this(num, 1);
	}

	/**
	 * Recupera il numeratore
	 * 
	 * @return Numeratore della frazione
	 */
	public int getNum() {
		return num;
	}

	/**
	 * Recupera il denominatore
	 * 
	 * @return Denominatore della frazione
	 */
	public int getDen() {
		return den;
	}

	/**
	 * Calcola la funzione ridotta ai minimi termini.
	 * 
	 * @return Una nuova funzione equivalente all'attuale, ridotta ai minimi
	 *         termini.
	 */
	public Frazione minTerm() {
		if (getNum()==0) return new Frazione(getNum(), getDen());
		int mcd = MyMath.mcd(Math.abs(getNum()), getDen());
		int n = getNum() / mcd;
		int d = getDen() / mcd;
		return new Frazione(n, d);
	}

	

	public boolean equals(Frazione f) {
		return f.getNum() * getDen() == f.getDen() * getNum();
	}

	@Override
	   public String toString() {
		   String str = "";
			int num = getNum();
			int den = getDen();

			str += getDen() == 1 ? num : num + "/" + den;		
			return str;	   
	   }
	
	
	public Frazione sum(Frazione f) {
		int n = (this.num * f.den + f.num * this.den);
		int d = (this.den * f.den);
		return new Frazione(n, d).minTerm();
	}
	
	public Frazione sumWithMcm(Frazione f) {
		int mcm = MyMath.mcm(f.den, this.den);
		int n1 = ((mcm/f.den)*f.num);
		int n2 = ((mcm/this.den)*this.num);
		return new Frazione(n1+n2, mcm).minTerm();
	}
	
	public Frazione sub(Frazione f) {
		int mcm = MyMath.mcm(f.den, this.den);
		int n1 = ((mcm/f.den)*f.num);
		int n2 = ((mcm/this.den)*this.num);
		return new Frazione(n2-n1, mcm).minTerm();
	}
	
	public Frazione mul(Frazione f) {
		int num = this.num * f.num;
		int den = this.den * f.den;
		return new Frazione(num,den).minTerm();
	}
	
	public Frazione div(Frazione f) {
		int num = this.num * f.reciprocal().num;
		int den = this.den * f.reciprocal().den;
		return new Frazione(num, den).minTerm();
	}
	
	public Frazione reciprocal() {
		int num = this.den;
		int den = this.num;
		return new Frazione(num, den).minTerm();
	}
	
	public int compareTo(Frazione f) {
		
		if (this.getDouble() - f.getDouble() > 0) {
			return 1;
		}else if (this.getDouble() - f.getDouble() < 0) {
			return -1;
		}else return 0;
		
	}
	
	public double getDouble() {
		return (double) this.num / this.den;
	}
	
}
