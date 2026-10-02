package frazione;
import util.MyMath;

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
	
	
	public static Frazione sum(Frazione[] fs) {
		Frazione sumTemp = new Frazione(0);
		for (int i = 0; i < fs.length && fs[i] != null; i++) {
			sumTemp = sumTemp.sumWithMcm(fs[i]);
		}
		return sumTemp;
	}
	
	public static Frazione mul(Frazione[] fs) {
		Frazione mulTemp = new Frazione(1);
		for (int i = 0; i < fs.length && fs[i] != null; i++) {
			mulTemp = mulTemp.mul(fs[i]);
		}
		return mulTemp;
	}
	
	public static String convertToString(Frazione[] fs) {
		String res = "[";
		for (int i = 0; i < fs.length && fs[i] != null; i++) {
			if(i != 0) res+= ", ";
			res += fs[i].toString();
		} 
		res += "]";
		return res;
	}
	
	public static int size(Frazione[] fs) {
		int size = 0;
		for (size = 0; size < fs.length && fs[size] != null; size++) {
			
		}
		return size;
	}
	
	
	public static Frazione[] sum(Frazione[] fA, Frazione[] fB) {
		if (size(fA) == size(fB)) {
			Frazione[] risultato = new Frazione[size(fA)];  
			for (int i = 0; i < fA.length && fA[i] != null; i++) {
				risultato[i] = fA[i].sumWithMcm(fB[i]);
			} return risultato;
		}else return null; 
	}
	
	public static Frazione[] mul(Frazione[] fA, Frazione[] fB) {
		if (size(fA) == size(fB)) {
			Frazione[] risultato = new Frazione[size(fA)];  
			for (int i = 0; i < fA.length && fA[i] != null; i++) {
				risultato[i] = fA[i].mul(fB[i]);
			} return risultato;
		}else return null; 
	}
	
	
	
	
	
	
	
}
