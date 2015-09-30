package com.hrc51.csu.andruino;

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
	JsonParser jp;
	HttpURLConnection urlConnection;
	private boolean authenticated;
	private boolean useSSL;
	private String serverURL;
	private String serverPort;
	private String username;
	private String password;
	private String cookieJar;

	public Webduino(SharedPreferences settings) {
		updateSettings(settings);
	}

	public void updateSettings(SharedPreferences settings){
		serverSettings = settings;
		useSSL = serverSettings.getBoolean("usessl", false);
		serverURL = serverSettings.getString("serverurl", "csu.hrc51.com");
		serverPort = serverSettings.getString("serverport", "8080");
	    username = serverSettings.getString("username", "matt");
	    password = serverSettings.getString("password", "password");
	}

	public boolean login() {
	       URL url;
	       try {
	    	   if (useSSL)
	        	   url = new URL("https://"+serverURL+":"+serverPort+"/login/"+username+"/"+password);
	    	   else // don't use ssl
	    		   url = new URL("http://"+serverURL+":"+serverPort+"/login/"+username+"/"+password);

	    	   urlConnection = (HttpURLConnection) url.openConnection();
	    	   cookieJar = urlConnection.getHeaderField("Set-Cookie");
	    	   
//	    	   BufferedReader in;
//	    	   try {
//		    	   in = new BufferedReader(new InputStreamReader(urlConnection.getInputStream()));
//		    	   String inputLine;
//		    	   inputLine = in.readLine();
//		    	   jp = new JsonParser(inputLine);
//		    	   in.close();
//	    	   }
//	    	   catch (IOException e){
//	    		   login();
//	    	   }
	    	   BufferedReader in;

		    	   in = new BufferedReader(new InputStreamReader(urlConnection.getInputStream()));
		    	   String inputLine;
		    	   inputLine = in.readLine();
		    	   jp = new JsonParser(inputLine);
		    	   in.close();

	    	   urlConnection.disconnect();

	    	   if (jp.getResponse().equals("pass"))
	    	   {
	    		   authenticated = true;
	    		   return true;
	    	   }
	    	   else
	    	   {
	    		   authenticated = false;
	    		   return false;
	    	   }
	       }
	       catch (MalformedURLException e) {
    		   authenticated = false;
	    	   return false;
	       }
	       catch (IOException e) {
    		   authenticated = false;
	    	   return false;
	       }
	}
	
	public boolean logout() {
	       if (!authenticated) return true;

	       URL url;
	       try {
	    	   if (useSSL)
	        	   url = new URL("https://"+serverURL+":"+serverPort+"/logout");
	    	   else // don't use ssl
	    		   url = new URL("http://"+serverURL+":"+serverPort+"/logout");

	    	   urlConnection = (HttpURLConnection) url.openConnection();
	    	   
	    	   BufferedReader in;
	    	   try {
		    	   in = new BufferedReader(new InputStreamReader(urlConnection.getInputStream()));
		    	   String inputLine;
		    	   inputLine = in.readLine();
		    	   jp = new JsonParser(inputLine);
		    	   in.close();
	    	   }
	    	   catch (IOException e){
	    		   logout();
	    	   }
	    	   
	    	   urlConnection.disconnect();
    		   authenticated = false;

	    	   if (jp.getResponse().equals("pass")) return true;
	    	   else return false;
	       }
	       catch (MalformedURLException e) { return false; }
	       catch (IOException e) { return false; }
	}
	
	public ArrayList<AndruinoObj> read() {
	       if (!authenticated) login();

	       URL url;
	       ArrayList<AndruinoObj> alError = new ArrayList<AndruinoObj>();
	       try {
	    	   if (useSSL)
	        	   url = new URL("https://"+serverURL+":"+serverPort+"/read");
	    	   else // don't use ssl
	    		   url = new URL("http://"+serverURL+":"+serverPort+"/read");

	    	   urlConnection = (HttpURLConnection) url.openConnection();
	    	   urlConnection.setRequestProperty("Cookie",cookieJar);
	    	   
	    	   BufferedReader in;
	    	   try {
		    	   in = new BufferedReader(new InputStreamReader(urlConnection.getInputStream()));
		    	   String inputLine;
		    	   inputLine = in.readLine();
		    	   jp = new JsonParser(inputLine);
		    	   in.close();
	    	   }
	    	   catch (IOException e){
	    		   read();
	    	   }
	    	   urlConnection.disconnect();
	    	   return jp.getDetails();
	       }
	       catch (MalformedURLException e) {
	    	   AndruinoObj errObj = new AndruinoObj(0,0,"URL Error",e.toString(),0,0,0,0,"");
	    	   alError.add(errObj);
	    	   return(alError);
	       }
	       catch (IOException e) {
	    	   AndruinoObj errObj = new AndruinoObj(0,0,"IO Error",e.toString(),0,0,0,0,"");
	    	   alError.add(errObj);
	    	   return(alError);
	       }
	}
	
	public boolean write(int did, int value) {
	       if (!authenticated) login();

	       URL url;
	       try {
	    	   if (useSSL)
	        	   url = new URL("https://"+serverURL+":"+serverPort+"/write/"+did+"/"+value);
	    	   else // don't use ssl
	    		   url = new URL("http://"+serverURL+":"+serverPort+"/write/"+did+"/"+value);

	    	   urlConnection = (HttpURLConnection) url.openConnection();
	    	   urlConnection.setRequestProperty("Cookie",cookieJar);
	    	   
	    	   BufferedReader in;
	    	   try {
		    	   in = new BufferedReader(new InputStreamReader(urlConnection.getInputStream()));
		    	   String inputLine;
		    	   inputLine = in.readLine();
		    	   jp = new JsonParser(inputLine);
		    	   in.close();
	    	   }
	    	   catch (IOException e){
	    		   write(did, value);
	    	   }
	    	   
	    	   urlConnection.disconnect();
	    	   
	    	   if (jp.getResponse().equals("pass")) return true;
	    	   else return false;
	       }
	       catch (MalformedURLException e) { return false; }
	       catch (IOException e) { return false; }
	}

	public boolean enable(boolean isEnabled, int did) {
	       if (!authenticated) login();

	       URL url;
    	   String action = isEnabled ? "enable" : "disable";
	       try {
	    	   if (useSSL)
	        	   url = new URL("https://"+serverURL+":"+serverPort+"/"+action+"/pin/"+did);
	    	   else // don't use ssl
	    		   url = new URL("http://"+serverURL+":"+serverPort+"/"+action+"/pin/"+did);

	    	   urlConnection = (HttpURLConnection) url.openConnection();
	    	   urlConnection.setRequestProperty("Cookie",cookieJar);

	    	   BufferedReader in;
	    	   try {
		    	   in = new BufferedReader(new InputStreamReader(urlConnection.getInputStream()));
		    	   String inputLine;
		    	   inputLine = in.readLine();
		    	   jp = new JsonParser(inputLine);
		    	   in.close();
	    	   }
	    	   catch (IOException e){
	    		   enable(isEnabled, did);
	    	   }
	    	   
	    	   urlConnection.disconnect();
	    	   
	    	   if (jp.getResponse().equals("pass")) return true;
	    	   else return false;
	       }
	       catch (MalformedURLException e) { return false; }
	       catch (IOException e) { return false; }
	}
	
	public boolean setLabel(int did, String newLabel) {
	       if (!authenticated) login();

	       URL url;
	       try {
	    	   if (useSSL)
	        	   url = new URL("https://"+serverURL+":"+serverPort+"/setlabel/pin/"+did+"/"+newLabel);
	    	   else // don't use ssl
	    		   url = new URL("http://"+serverURL+":"+serverPort+"/setlabel/pin/"+did+"/"+newLabel);

	    	   urlConnection = (HttpURLConnection) url.openConnection();
	    	   urlConnection.setRequestProperty("Cookie",cookieJar);
	    	   
	    	   BufferedReader in;
	    	   try {
		    	   in = new BufferedReader(new InputStreamReader(urlConnection.getInputStream()));
		    	   String inputLine;
		    	   inputLine = in.readLine();
		    	   jp = new JsonParser(inputLine);
		    	   in.close();
	    	   }
	    	   catch (IOException e){
	    		   setLabel(did, newLabel);
	    	   }
	    	   
	    	   urlConnection.disconnect();

	    	   if (jp.getResponse().equals("pass")) return true;
	    	   else return false;
	       }
	       catch (MalformedURLException e) { return false; }
	       catch (IOException e) { return false; }
	}
}
