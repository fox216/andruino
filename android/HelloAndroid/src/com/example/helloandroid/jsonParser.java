package com.example.helloandroid;

import org.json.JSONArray;
import org.json.JSONObject;

public class jsonParser {
	private JSONObject jObject;

	public jsonParser(String jsonString) {
		try {
			jObject = new JSONObject(jsonString);
		}
		catch (Exception e) {
			//e.toString();
		}
	}

	public String getValueByName(String name) {
		try {
				return jObject.getString(name);
			}
		catch (Exception e) {
			return e.toString();
		}
	}
	
	public void parse() throws Exception {
		JSONObject menuObject = jObject.getJSONObject("menu");
		String attributeId = menuObject.getString("id");
		System.out.println(attributeId);

		String attributeValue = menuObject.getString("value");
		System.out.println(attributeValue);

		JSONObject popupObject = menuObject.getJSONObject("popup");
		JSONArray menuitemArray = popupObject.getJSONArray("menuitem");

		for (int i = 0; i < 3; i++) {
			System.out.println(menuitemArray.getJSONObject(i)
					.getString("value").toString());
			System.out.println(menuitemArray.getJSONObject(i).getString(
					"onclick").toString());
		}
	}



}
