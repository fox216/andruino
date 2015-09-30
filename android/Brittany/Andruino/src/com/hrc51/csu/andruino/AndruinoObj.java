package com.hrc51.csu.andruino;

public class AndruinoObj {
	private int did;
	private int id;
	private String label;
	private String device;
	private int ddr;
	private int pin;
	private int value;
	private int enabled;
	private String ts_value;
//	private boolean notify;
	
	public AndruinoObj()
	{

	}
	
	public AndruinoObj(int did, int id, String label, String device, int ddr, int pin, int value, int enabled, String ts_value/*, boolean notify */)
	{
		this.did = did;
		this.id = id;
		this.label = label;
		this.device = device;
		this.ddr = ddr;
		this.pin = pin;
		this.value = value;
		this.enabled = enabled;
		this.ts_value = ts_value;
	}

	public int getDid() {
		return did;
	}

	public void setDid(int did) {
		this.did = did;
	}

	public int getId() {
		return id;
	}

	public void setId(int id) {
		this.id = id;
	}

	public String getLabel() {
		return label;
	}

	public void setLabel(String label) {
		this.label = label;
	}

	public String getDevice() {
		return device;
	}

	public void setDevice(String device) {
		this.device = device;
	}
	
	public int getDdr() {
		return ddr;
	}

	public void setDdr(int ddr) {
		this.ddr = ddr;
	}

	public int getPin() {
		return pin;
	}

	public void setPin(int pin) {
		this.pin = pin;
	}

	public int getValue() {
		return value;
	}

	public void setValue(int value) {
		this.value = value;
	}
	
	public int getEnabled() {
		return enabled;
	}

	public void setEnabled(int enabled) {
		this.enabled = enabled;
	}

	public String getTs_value() {
		return ts_value;
	}

	public void setTs_value(String ts_value) {
		this.ts_value = ts_value;
	}
	
//	public boolean isNotify() {
//		return notify;
//	}
//
//	public void setNotify(boolean notify) {
//		this.notify = notify;
//	}

	
}

