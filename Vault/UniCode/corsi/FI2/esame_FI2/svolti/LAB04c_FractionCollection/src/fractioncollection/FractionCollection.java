package fractioncollection;
import frazione.Frazione;



public class FractionCollection {

	private static final int DEFAULT_GROWTH_FACTOR = 2;
	private static final int DEFAULT_PHYSICAL_SIZE = 10;
	
	private Frazione[] innerContainer;
	private int size;
	
	public FractionCollection(int physicalSize) {
		innerContainer = new Frazione[physicalSize];
		size = 0;
	}
	
	public FractionCollection() {
		innerContainer = new Frazione[DEFAULT_PHYSICAL_SIZE];
	}
	
	public FractionCollection(Frazione[] collection) {
		size = Frazione.size(collection);
		innerContainer = new Frazione[size];
		for (int i = 0; i < size; i++) {
			innerContainer[i] = collection[i];
		}
	}
	
	public Frazione get(int index) {	//
		if (index < 0 || index >= size) 
			throw new IndexOutOfBoundsException("indice " + index + " fuori dalla dimensione logica dell'array (" + size + ")");
		else return this.innerContainer[index];
	}
	
	public int size() {	//dimensione logica della collection
		return size;
	}
	
	public void put(Frazione f) {
		if (this.innerContainer.length == 0) {
			this.innerContainer = new Frazione[DEFAULT_PHYSICAL_SIZE];
		}
		if (this.size == innerContainer.length) {
			Frazione[] fs = new Frazione[innerContainer.length * DEFAULT_GROWTH_FACTOR];
			for(int i = 0; i < size; i++) {
				fs[i] = this.innerContainer[i];
			}
			this.innerContainer = fs;
		}
			
		this.innerContainer[size] = f;
		size++;
	}
	
	public void remove(int index) {
		if (index >= 0 && index < size) {
			int i = 0;
			for(i = index; i < size-1; i++) {
				this.innerContainer[i] = this.innerContainer[i+1];
			}
			this.innerContainer[i] = null;
			size--;
		}else throw new IndexOutOfBoundsException("indice " + index + " fuori dalla dimensione logica dell'array (" + size + ")");
	}
	
	public FractionCollection sum (FractionCollection collection) {
		if(this.size == collection.size) {
			FractionCollection res = new FractionCollection(size);
			for(int i = 0; i < size; i++) {
				res.put(this.get(i).sumWithMcm(collection.get(i)));
			}
			return res;
		}else throw new IllegalArgumentException("Dimensioni logiche degli array divese");

	}
	
	public FractionCollection mul (FractionCollection collection) {
		if(this.size == collection.size) {
			FractionCollection res = new FractionCollection(size);
			for(int i = 0; i < size; i++) {
				res.put(this.get(i).mul(collection.get(i)));
			}
			return res;
		}else throw new IllegalArgumentException("Dimensioni logiche degli array divese");

	}
	
	public String toString() {
		StringBuilder sb = new StringBuilder();
		sb.append("[ ");
		for(int i = 0; i < size; i++) {
			if(i!=0) {
				sb.append(", ");
			}
			sb.append(this.innerContainer[i]);
		}
		sb.append(" ]");
		String res = sb.toString();
		return res;
	}
	
	
	
	
	
	
	
	
	
	
	
	
}
