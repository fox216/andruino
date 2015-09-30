package com.hrc51.csu.andruino;

import java.util.ArrayList;
import org.json.JSONArray;
import org.json.JSONObject;

public class JsonParser {
	private JSONObject jObject;
	private JSONArray detailArray;
	private String command;
	private String response;

	public JsonParser(String jsonString) {
		try {
			jObject = new JSONObject(jsonString);
			command = getValueByName("command");
	    	response = getValueByName("response");
	    	detailArray = jObject.getJSONArray("details");
		}
		catch (Exception e) {
			e.printStackTrace();
		}
	}

	public String getCommand() {
		return command;
	}

	public String getResponse() {
		return response;
	}

	public ArrayList<AndruinoObj> getDetails() {
		ArrayList<AndruinoObj> detailList = new ArrayList<AndruinoObj>();
		try {
			for (int i = 0; i < Integer.parseInt(response); i++) {
				int did = Integer.parseInt(detailArray.getJSONObject(i).getString("did"));
				int id = Integer.parseInt(detailArray.getJSONObject(i).getString("id"));
				String label = detailArray.getJSONObject(i).getString("label").trim();
				String device = detailArray.getJSONObject(i).getString("device").trim();;
				int ddr = Integer.parseInt(detailArray.getJSONObject(i).getString("ddr"));
				int pin = Integer.parseInt(detailArray.getJSONObject(i).getString("pin"));
				int value = Integer.parseInt(detailArray.getJSONObject(i).getString("value"));
				int enabled = Integer.parseInt(detailArray.getJSONObject(i).getString("enabled"));
				String ts_value = detailArray.getJSONObject(i).getString("ts_value").trim();
//				boolean notify = detailArray.getJSONObject(i).getString("notify").equals("1") ? true : false;
				
				AndruinoObj controlElt = new AndruinoObj(did, id, label, device, ddr, pin, value, enabled, ts_value/*, notify */);
				detailList.add(controlElt);
			}
		}
		catch (Exception e) {
			e.printStackTrace();
		}

		return detailList;
	}
	
	public String getValueByName(String name) {
		try {
			return jObject.getString(name);
		}
		catch (Exception e) {
			return e.toString();
		}
	}
}

