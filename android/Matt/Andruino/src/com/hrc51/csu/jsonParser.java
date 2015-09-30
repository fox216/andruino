package com.hrc51.csu;

import java.util.ArrayList;
import org.json.JSONArray;
import org.json.JSONObject;

public class jsonParser {
	private JSONObject jObject;
	private JSONArray detailArray;
	private String command;
	private String response;

	public jsonParser(String jsonString) {
		try {
			jObject = new JSONObject(jsonString);
			command = getValueByName("command");
	    	response = getValueByName("response");
	    	detailArray = jObject.getJSONArray("details");
		}
		catch (Exception e) {}
	}

	public String getCommand() {
		return command;
	}

	public String getResponse() {
		return response;
	}

	public ArrayList<String> getDetails() {
		ArrayList<String> detailList = new ArrayList<String>();
		try {
			for (int i = 0; i < Integer.parseInt(response); i++) {
				detailList.add(detailArray.getJSONObject(i).getString("label").toString());
			}
		}
		catch (Exception e) {}

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
