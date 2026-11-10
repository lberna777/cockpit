package edlift.model.util;

public class Queue {

	private int booked;
	private int[] bookings;
	private int maxBookings;
	
	public Queue(int maxBookings) {
		super();
		this.maxBookings = maxBookings;
		this.bookings = new int[maxBookings];
		booked = 0;
	}
	
	public boolean insert(int n) {
		if(booked == bookings.length) {
			return false;
		}
		
		bookings[booked] = n;
		booked++;
		return true;
	}
	
	public int size() {
		return booked;
	}
	
	public boolean hasItems() {
		if (booked != 0) {
			return true;
		} else return false;
	}
	
	public int peek() {
		return bookings[booked];
	}
	
	public int extract() {
		
		int ret = bookings[0];
		for (int i = 0; i < booked-1; i++) {
			bookings[i] = bookings[i+1];
		}
		booked--;
		return ret;
	}
	

}
