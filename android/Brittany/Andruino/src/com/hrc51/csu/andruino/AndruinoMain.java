package com.hrc51.csu.andruino;

import android.app.TabActivity;
import android.content.Intent;
import android.content.res.Resources;
import android.os.Bundle;
import android.widget.TabHost;
import android.widget.TabHost.TabSpec;

public class AndruinoMain extends TabActivity {
	
	public void onCreate(Bundle savedInstanceState) {
	    super.onCreate(savedInstanceState);
	    setContentView(R.layout.main);

	    Resources res = getResources();
	    TabHost tabHost = getTabHost(); 
	    TabSpec spec; 
	    Intent intent;  

	    // Create an Intent to launch an Activity for the tab (to be reused)
	    intent = new Intent().setClass(this, Indicators.class);

	    // Initialize a TabSpec for each tab and add it to the TabHost
	    spec = tabHost.newTabSpec("indicators").setIndicator("Indicators", res.getDrawable(R.drawable.ic_tab_indicators)).setContent(intent);
	    tabHost.addTab(spec);

	    // Do the same for the other tabs
	    intent = new Intent().setClass(this, Outputs.class);
	    spec = tabHost.newTabSpec("outputs").setIndicator("Outputs", res.getDrawable(R.drawable.ic_tab_outputs)).setContent(intent);
	    tabHost.addTab(spec);

	    tabHost.setCurrentTab(0);
	}

}
