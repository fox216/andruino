package com.example.helloandroid;

import android.app.Activity;
import android.content.Intent;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.preference.PreferenceManager;
import android.view.Menu;
import android.view.MenuInflater;
import android.view.MenuItem;
import android.widget.TextView;
import android.widget.Toast;

public class HelloAndroid extends Activity {
   SharedPreferences settings;
   Webduino wc;

   /** Called when the activity is first created. */
   @Override
   public void onCreate(Bundle savedInstanceState) {
       super.onCreate(savedInstanceState);
       TextView tv = new TextView(this);

       settings = PreferenceManager.getDefaultSharedPreferences(this);
       wc = new Webduino(settings);

       tv.setText(wc.read());
       setContentView(tv);
    }

	@Override
	public boolean onCreateOptionsMenu(Menu menu) {
		MenuInflater inflater = getMenuInflater();
		inflater.inflate(R.menu.menu, menu);
		return true;
	}

	@Override
	public boolean onOptionsItemSelected(MenuItem item) {
		//Toast.makeText(this, "Just a test", Toast.LENGTH_SHORT).show();
		
		switch (item.getItemId()) {
			// We have only one menu option
			case R.id.settings:
				// Launch Preference activity
				Intent i = new Intent(HelloAndroid.this, Settings.class);
				startActivity(i);
				// Some feedback to the user
				Toast.makeText(HelloAndroid.this,
						"Here you can maintain your server settings and user credentials.",
						Toast.LENGTH_LONG).show();
				break;
			case R.id.refresh:
				
				break;
		}
		
		return true;
	}
}