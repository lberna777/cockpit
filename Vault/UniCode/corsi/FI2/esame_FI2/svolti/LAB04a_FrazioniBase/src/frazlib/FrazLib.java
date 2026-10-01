package frazlib;

import frazione.Frazione;

public class FrazLib {
	
	
	public static Frazione sum(Frazione[] fs) {
		Frazione sumTemp = new Frazione(0);
		for (Frazione f : fs) {
			sumTemp = sumTemp.sum(f);
		}
		return sumTemp;
	}
	
	public static Frazione mul(Frazione[] fs) {
		Frazione mulTemp = new Frazione(1);
		for (Frazione f : fs) {
			mulTemp = mulTemp.mul(f);
		}
		return mulTemp;
	}

}
