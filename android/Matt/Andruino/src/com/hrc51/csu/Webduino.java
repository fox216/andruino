package com.hrc51.csu;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.MalformedURLException;
import java.net.URL;
import java.util.ArrayList;
import android.content.SharedPreferences;

public class Webduino {
	SharedPreferences serverSettings;
	jsonParser jp;

	public Webduino(SharedPreferences settings) {
		serverSettings = settings;
	}
	
	public String index() {
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
	    	   response = "Command: " + jp.getCommand() + "\n";
	    	   response += "Response: " + jp.getResponse() + "\n";
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
	public ArrayList<String> read() {
	       URL url;
	       HttpURLConnection urlConnection;
	       ArrayList<String> alError = new ArrayList<String>();

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
	    	   
	    	   in.close();
	    	   urlConnection.disconnect();
	    	   return jp.getDetails();
	       }
	       catch (MalformedURLException e) {
	    	   alError.add("url Error" +e);
	    	   return(alError);
	       }
	       catch (IOException e) {
	    	   alError.add("IO Error: "+e);
	    	   return(alError);
	       }
	}
}
