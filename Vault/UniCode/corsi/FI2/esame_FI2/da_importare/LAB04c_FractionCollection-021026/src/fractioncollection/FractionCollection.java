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
	
	
	
	
	
	
	
	
	
}
