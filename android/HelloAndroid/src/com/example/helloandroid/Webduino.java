package com.example.helloandroid;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.MalformedURLException;
import java.net.URL;

import android.content.SharedPreferences;


public class Webduino {
	SharedPreferences serverSettings;

	public Webduino(SharedPreferences settings) {
		serverSettings = settings;
	}
	
	public String index() {
	       jsonParser jp;
	       URL url;
	       HttpURLConnection urlConnection;
	       String response;

	       try {
	    	   if (serverSettings.getBoolean("usessl", false))
	        	   url = new URL("https://"+serverSettings.getString("serverurl", "n/a")+":"+serverSettings.getString("serverport", "n/a")+"/");
	    	   else
	    		   url = new URL("http://"+serverSettings.getString("serverurl", "n/a")+":"+serverSettings.getString("serverport", "n/a")+"/");
	    	   urlConnection = (HttpURLConnection) url.openConnection();
	    	   BufferedReader in = new BufferedReader(new InputStreamReader(urlConnection.getInputStream()));
	    	   String inputLine;
	    	   inputLine = in.readLine();
	    	   jp = new jsonParser(inputLine);
	    	   response = "Command: " + jp.getValueByName("command") + "\n";
	    	   response += "Response: " + jp.getValueByName("response") + "\n";
	    	   in.close();
	    	   urlConnection.disconnect();
	    	   return response;
	       }
	       catch (MalformedURLException e) {
	    	   return("url Error");
	       }
	       catch (IOException e) {
	    	   return("IO Error: "+e);
	       }
	}
	public String read() {
	       jsonParser jp;
	       URL url;
	       HttpURLConnection urlConnection;
	       String response;

	       try {
	    	   if (serverSettings.getBoolean("usessl", false))
	        	   url = new URL("https://"+serverSettings.getString("serverurl", "n/a")+":"+serverSettings.getString("serverport", "n/a")+"/read");
	    	   else
	    		   url = new URL("http://"+serverSettings.getString("serverurl", "n/a")+":"+serverSettings.getString("serverport", "n/a")+"/read");
	    	   urlConnection = (HttpURLConnection) url.openConnection();
	    	   BufferedReader in = new BufferedReader(new InputStreamReader(urlConnection.getInputStream()));
	    	   String inputLine;
	    	   inputLine = in.readLine();
	    	   jp = new jsonParser(inputLine);
	    	   response = "Command: " + jp.getValueByName("command") + "\n";
	    	   response += "Response: " + jp.getValueByName("response") + "\n";
	    	   response += "Details: " + jp.getValueByName("details");
	    	   in.close();
	    	   urlConnection.disconnect();
	    	   return response;
	       }
	       catch (MalformedURLException e) {
	    	   return("url Error");
	       }
	       catch (IOException e) {
	    	   return("IO Error: "+e);
	       }
	}
}
