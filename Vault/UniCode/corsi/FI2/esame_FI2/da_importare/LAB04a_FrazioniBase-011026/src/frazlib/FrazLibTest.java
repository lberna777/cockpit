package frazlib;


import frazione.Frazione;

public class FrazLibTest {
	
	
	public static void main(String[] args) {
		  Frazione[] frazioni = new Frazione[4]; 
		  frazioni[0]= new Frazione(1,3);
		  frazioni[1]= new Frazione(2,3);
		  frazioni[2]= new Frazione(-1,2);
		  frazioni[3]= new Frazione(1,6);
		  Frazione somma= FrazLib.sum(frazioni);
		  assert(somma.getNum() == 2 && somma.getDen() == 3);
		  Frazione mul= FrazLib.mul(frazioni);
		  assert(mul.getNum() == -1 && mul.getDen() == 54);
		 
		  
		  frazioni = new Frazione[4]; 
		  frazioni[0] = new Frazione(1,5);
		  frazioni[1] = new Frazione(2,8);
		  frazioni[2] = new Frazione(1,7);
		  frazioni[3] = new Frazione(-1,6);
		  somma = FrazLib.sum(frazioni);
		  assert(somma.getNum() == 179 && somma.getDen() == 420);
		   mul= FrazLib.mul(frazioni);
		  assert(mul.getNum() == -1 && mul.getDen() == 840);
		    
	 }
}



