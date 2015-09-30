package com.hrc51.csu.andruino;

import java.util.ArrayList;


import android.app.AlertDialog;
import android.app.ListActivity;
import android.app.ProgressDialog;
import android.content.DialogInterface;
import android.content.Intent;
import android.content.SharedPreferences;
import android.os.AsyncTask;
import android.os.Bundle;
import android.preference.PreferenceManager;
import android.view.ContextMenu;
import android.view.LayoutInflater;
import android.view.Menu;
import android.view.MenuInflater;
import android.view.MenuItem;
import android.view.View;
import android.widget.AdapterView.AdapterContextMenuInfo;
import android.widget.EditText;
import android.widget.LinearLayout;
import android.widget.ListView;
import android.widget.TextView;
import android.widget.Toast;

public class Outputs extends ListActivity {
	private ArrayList<AndruinoObj> allControls;
	private ArrayList<AndruinoObj> deviceOutputs;
	private IOAdapter ctrl_adapter; 
	private SharedPreferences settings;
	private Webduino wc;
	private AndruinoObj selectedObj;
	private EditText labelEdit;
	
	/** Called when the activity is first created. */
    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.outputs);
        settings = PreferenceManager.getDefaultSharedPreferences(this);
		wc = new Webduino(settings);
        allControls = wc.read();
		deviceOutputs = filterControls(allControls);
        
		new RetrieveControlsTask().execute();
    }
    
	@Override
	public boolean onCreateOptionsMenu(Menu menu) {
		MenuInflater inflater = getMenuInflater();
		inflater.inflate(R.menu.options_menu, menu);
		return true;
	}

	@Override
	public boolean onOptionsItemSelected(MenuItem item) {
		switch (item.getItemId()) 
		{
		case R.id.settings:
			// Launch Preference activity
			Intent i = new Intent(this, Settings.class);
			startActivity(i);
			// Some feedback to the user
			Toast.makeText(this,
					"Here you can maintain your server settings and user credentials.",
					Toast.LENGTH_LONG).show();
			break;
			
		case R.id.refresh:
			new RetrieveControlsTask().execute();
			break;
			
		case R.id.help:
			startActivity(new Intent(this, Help.class));
			break;
			
		case R.id.about:
			AlertDialog.Builder about = new AlertDialog.Builder(Outputs.this);
	    	about.setTitle("Andruino 1.0.0");
	    	about.setMessage("\u00a9" + " 2011 by Brittany Jones, Matt Kunkel, Kevin Fox, Sushant Arora. All Rights Reserved.");
	    	
	    	about.setPositiveButton("OK", new DialogInterface.OnClickListener() {
			
				public void onClick(DialogInterface dialog, int which) {
					dialog.dismiss();
				}
			});
	    	about.show();
			break;
			
		case R.id.login:
			int itr = 1;
			while(itr <= 3)
			{
				itr++;
				if(wc.login()) 
				{
					new RetrieveControlsTask().execute();
					break;
				}
			}
			if(itr == 3)
			{
				Toast.makeText(this,
					"Cannot connect to server. Check your settings.",
					Toast.LENGTH_LONG).show();
			}
			break;
		}

		return true;
	}
	
	@Override
	public void onCreateContextMenu(ContextMenu menu, View v, ContextMenu.ContextMenuInfo menuInfo) {
		MenuInflater inflater = getMenuInflater();
        inflater.inflate(R.menu.context_menu, menu);
        AdapterContextMenuInfo info = (AdapterContextMenuInfo) menuInfo;
        LinearLayout tView = (LinearLayout)info.targetView;
        TextView outName = (TextView)tView.findViewById(R.id.output_name);
        menu.setHeaderTitle(outName.getText().toString());
    }

	@Override
	public boolean onContextItemSelected(MenuItem item) {
	  AdapterContextMenuInfo info = (AdapterContextMenuInfo) item.getMenuInfo();
	  LinearLayout tView = (LinearLayout)info.targetView;
      TextView outName = (TextView)tView.findViewById(R.id.output_name);
      String pinName = outName.getText().toString();
      selectedObj = getObjByName(pinName);
	  
      switch(item.getItemId())
	  {
	  case R.id.edit_name:
		  // allow user to edit name of pin
		  AlertDialog.Builder alert = new AlertDialog.Builder(this);
		  LayoutInflater factory = LayoutInflater.from(this);
          final View textEntryView = factory.inflate(R.layout.edit_pin_dialog, null);          
          labelEdit = (EditText)textEntryView.findViewById(R.id.label_edit);
          labelEdit.setText(pinName);
          labelEdit.setSelectAllOnFocus(true);
          
		  alert.setTitle("Edit Pin Name");
		  alert.setView(textEntryView);
		  alert.setPositiveButton("OK", new DialogInterface.OnClickListener() {
			  public void onClick(DialogInterface dialog, int which) {
				  String newLabel = labelEdit.getText().toString();
				  wc.setLabel(selectedObj.getId(), newLabel);
				  refresh();
			  }
		  });
		  alert.setNegativeButton("Cancel", new DialogInterface.OnClickListener() {
			  public void onClick(DialogInterface dialog, int which) {}
		  });
		  alert.show();
		  break;
		  
	  case R.id.disable_enable:
		  // disable item if it's initially enabled
		  if(selectedObj.getEnabled() == 1)
			  wc.enable(false, selectedObj.getId());
		  // else restore menu item if it's initially disabled
		  else
			  wc.enable(true, selectedObj.getId());
		  refresh();
		  break;
	  }

	  return super.onContextItemSelected(item);
	}
	
	public void refresh() {
		  deviceOutputs = filterControls(wc.read());
	      ctrl_adapter = new IOAdapter(this, R.layout.output_row, deviceOutputs, wc);
	      setListAdapter(ctrl_adapter);
	      registerForContextMenu(getListView());
	}
	
	public ArrayList<AndruinoObj> filterControls(ArrayList<AndruinoObj> controls) {
		ArrayList<AndruinoObj> deviceOutputs = new ArrayList<AndruinoObj>();
		
		for(AndruinoObj obj : controls)
		{
			if (obj.getDdr() == 1) 
				deviceOutputs.add(obj);
		}
		return deviceOutputs;
	}
	
	public AndruinoObj getObjByName(String name) {
		AndruinoObj andrObj = new AndruinoObj();
		for(AndruinoObj obj : deviceOutputs)
		{
			if(obj.getLabel().equals(name))
				andrObj = obj;
		}
		
		return andrObj;
	}
	
	class RetrieveControlsTask extends AsyncTask<Void, AndruinoObj, Void> {
		ProgressDialog progress;
		protected void onPreExecute()
		{
			progress = ProgressDialog.show(Outputs.this,"Please wait...", "Retrieving data from " + settings.getString("serverurl", null) + "...", true);
		}
		
		@Override
		protected Void doInBackground(Void... unused) {
	        allControls = wc.read();
	        publishProgress();
	        return null;
		}

		@Override
		protected void onPostExecute(Void unused) {
			progress.dismiss();
			
            deviceOutputs = filterControls(allControls);
	        ctrl_adapter = new IOAdapter(Outputs.this, R.layout.output_row, deviceOutputs, wc);
	        setListAdapter(ctrl_adapter);
	        
	        ListView outputList = Outputs.this.getListView();
	        registerForContextMenu(outputList);
		}
	}
}