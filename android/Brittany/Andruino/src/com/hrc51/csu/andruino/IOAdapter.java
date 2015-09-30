package com.hrc51.csu.andruino;

import java.util.ArrayList;

import android.app.AlertDialog;
import android.content.Context;
import android.content.DialogInterface;
import android.content.SharedPreferences;
import android.graphics.Color;
import android.preference.PreferenceManager;
import android.view.ContextMenu;
import android.view.ContextMenu.ContextMenuInfo;
import android.view.LayoutInflater;
import android.view.View;
import android.view.View.OnClickListener;
import android.view.View.OnCreateContextMenuListener;
import android.view.ViewGroup;
import android.widget.ArrayAdapter;
import android.widget.ImageView;
import android.widget.TextView;

public class IOAdapter extends ArrayAdapter<AndruinoObj> {
    private ArrayList<AndruinoObj> controls;
    private Context context;
    private int textViewResourceId;
    private Webduino wc;
    private SharedPreferences settings;
    
    public IOAdapter(Context context, int textViewResourceId, ArrayList<AndruinoObj> controls, Webduino wc) {
            super(context, textViewResourceId, controls);
            this.context = context;
            this.textViewResourceId = textViewResourceId;
            this.controls = controls;
            this.wc = wc;
            this.settings = PreferenceManager.getDefaultSharedPreferences(context);
    }
    
    @Override
    public View getView(int position, View convertView, ViewGroup parent) {
    	View v = convertView;
            if (v == null) {
                LayoutInflater vi = (LayoutInflater)context.getSystemService(Context.LAYOUT_INFLATER_SERVICE);
                v = vi.inflate(textViewResourceId, null);
                
                // adding this listener so that the checkboxes in each row don't swallow the on-click event
                v.setOnCreateContextMenuListener(new OnCreateContextMenuListener()
                	{
                		public void onCreateContextMenu(ContextMenu contextMenu, View view, ContextMenuInfo arg2) {}
                	});
            }
            
            final AndruinoObj andrObj = controls.get(position);
           
            switch(textViewResourceId)
            {
            case R.layout.indicator_row:
            	if (andrObj != null) {
                    ImageView indicateState = (ImageView) v.findViewById(R.id.indicate_state);
            		TextView indicatorName = (TextView) v.findViewById(R.id.indicator_name);
                    TextView deviceName = (TextView) v.findViewById(R.id.device_name_ind);
                    //CheckBox notify = (CheckBox)v.findViewById(R.id.notify);
                    if(indicateState != null)
                    {
                    	int resourceId = andrObj.getValue() == 1 ? R.drawable.control_on : R.drawable.control_off;
                    	indicateState.setImageResource(resourceId);
                    }
                    if (indicatorName != null) 
                          indicatorName.setText(andrObj.getLabel());                            
                    if(deviceName != null)
                          deviceName.setText("Device: " + andrObj.getDevice() + ", Pin: " + andrObj.getId());
                    if(andrObj.getEnabled() == 0)
                    {
          			  indicateState.setImageResource(R.drawable.control_disable);
          			  indicatorName.setTextColor(Color.DKGRAY);
          			  deviceName.setTextColor(Color.DKGRAY);
          			  //notify.setEnabled(false);
                    }
                    else
                    {
                    	indicatorName.setTextColor(Color.WHITE);
            			deviceName.setTextColor(Color.WHITE);
            			//notify.setEnabled(true);
                    }
//                    if(notify != null)
//                    	notify.setChecked(andrObj.isNotify());
//                    	notify.setChecked(true);
	            }
            	break;
            
            case R.layout.output_row:
	            if (andrObj != null) {
                    TextView outputName = (TextView)v.findViewById(R.id.output_name);
                    TextView deviceName = (TextView)v.findViewById(R.id.device_name_out);
                    final String displayName = andrObj.getLabel();
                    final NewToggleButton tb = (NewToggleButton)v.findViewById(R.id.change_state);
                    
                    if (outputName != null) {
                          outputName.setText(andrObj.getLabel()); 
                    }
                    if(deviceName != null){
                          deviceName.setText("Device: " + andrObj.getDevice() + ", Pin: " + andrObj.getId());
                    }
                    if(tb != null){
                    	tb.setChecked(andrObj.getValue() == 1 ? true : false);
                    	if(settings.getBoolean("confirmation", false)){
	                    	tb.setOnClickListener(new OnClickListener() {
	                    	    public void onClick(View v) {
	
	                    	    	AlertDialog.Builder alert = new AlertDialog.Builder(context);
	                    	    	alert.setTitle("Confirm State Change");
	                    	    	alert.setIcon(android.R.drawable.ic_dialog_alert);
	                    	    	alert.setMessage("Are you sure you want to change the state of " + displayName + " to " + (andrObj.getValue() == 1 ? 0 : 1) +"?");
	                    	    	
	                    	    	alert.setPositiveButton("Yes", new DialogInterface.OnClickListener() {
									
										public void onClick(DialogInterface dialog, int which) {
											tb.setChecked(andrObj.getValue() == 1 ? false : true);
											andrObj.setValue(andrObj.getValue() == 1 ? 0 : 1);
											wc.write(andrObj.getId(), andrObj.getValue());
										}
									});
	                    	    	alert.setNegativeButton("No", new DialogInterface.OnClickListener() {
										
										public void onClick(DialogInterface dialog, int which) {}
									});
	                    	    	alert.show();
	                    	    }
	                    	});
                    	}
                    	else {
	                    	tb.setOnClickListener(new OnClickListener() {
	                    	    public void onClick(View v) {
	                    	    	tb.setChecked(andrObj.getValue() == 1 ? false : true);
									andrObj.setValue(andrObj.getValue() == 1 ? 0 : 1);
									wc.write(andrObj.getId(), andrObj.getValue());
	                    	    }
	                    	});
                    	}
                    }
                    if(andrObj.getEnabled() == 0)
                    {
                    	tb.setPressed(false); 
                    	tb.setEnabled(false);
                    	outputName.setTextColor(Color.DKGRAY);
          			  	deviceName.setTextColor(Color.DKGRAY);
                    }
                    else
                    {
                    	tb.setEnabled(true);
                    	outputName.setTextColor(Color.WHITE);
            			deviceName.setTextColor(Color.WHITE);
                    }
	            }
            	break;
            }
	        return v;
    }
}