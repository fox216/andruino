package com.example.helloandroid;

import android.app.Activity;
import android.os.Bundle;
import android.widget.TextView;
import java.net.*;
import java.io.*;

public class HelloAndroid extends Activity {
   /** Called when the activity is first created. */
   @Override
   public void onCreate(Bundle savedInstanceState) {
       super.onCreate(savedInstanceState);
       TextView tv = new TextView(this);

       URL url;
       HttpURLConnection urlConnection;

       try {
    	   url = new URL("https://csu.hrc51.com:8080/");
    	   //url = new URL("http://google.com/");
    	   urlConnection = (HttpURLConnection) url.openConnection();
    	   BufferedReader in = new BufferedReader(new InputStreamReader(urlConnection.getInputStream()));
    	   String inputLine;
    	   while ((inputLine = in.readLine()) != null)
    			   tv.setText(inputLine);
    	   in.close();
    	   urlConnection.disconnect();
       }
       catch (MalformedURLException e) {
    	   tv.setText("url Error");
       }
       catch (IOException e) {
    	   tv.setText("IO Error: "+e);
       }
       setContentView(tv);
    }
}