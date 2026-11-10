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
		if (booked > 0) {
			return bookings[0];
		}else return Integer.MIN_VALUE;
	}
	
	public int extract() {
		if (booked > 0) {
			int ret = bookings[0];
			for (int i = 0; i < booked-1; i++) {
				bookings[i] = bookings[i+1];
			}
			booked--;
			return ret;
		} else return Integer.MIN_VALUE;
	}
	

}
