package com.hrc51.csu.andruino;

import android.app.Activity;
import android.os.Bundle;
import android.widget.TextView;

public class Help extends Activity {
    /** Called when the activity is first created. */
    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.help);
        
        // defining views for this activity
        TextView helpIntro = (TextView)findViewById(R.id.helpIntro);
        TextView checkState = (TextView)findViewById(R.id.checkState);
//        TextView enableNotification = (TextView)findViewById(R.id.enableNotification);
        TextView editIndName = (TextView)findViewById(R.id.editIndName);
        TextView enableInd = (TextView)findViewById(R.id.enableInd);
        TextView changeState = (TextView)findViewById(R.id.changeState);
        TextView editOutName = (TextView)findViewById(R.id.editOutName);
        TextView enableOut = (TextView)findViewById(R.id.enableOut);
        TextView editServerInfo = (TextView)findViewById(R.id.editServerInfo);
        TextView enableHTTPS = (TextView)findViewById(R.id.enableHTTPS);
        TextView editCredentials = (TextView)findViewById(R.id.editCredentials);
        TextView enableConfirm = (TextView)findViewById(R.id.enableConfirm);

        
        // defining information to be displayed in the TextViews
        String intro = "This page provides instructions for how to perform the basic functions of the " +
        		"Andruino application. Instructions for the different functionalities are grouped according " +
        		"to the page from which you can perform that functionality.\n";
        String check = "You can monitor the state of the input from the Indicators page. The state of an " +
        		"input is indicated by the color of the circle on the left-hand side of the indicator name. " +
        		"Red indicates that the input is \"off,\" green indicates that it is \"on\" and grey " +
        		"indicates that it is \"disabled.\"\n";
//        String enableN = "You can enable email notifications for a particular input by simply checking the" +
//        		" box next to the indicator for which you want notifications.\n";
        String editI = "To edit the name of an input, long-press on the item which will cause a context " +
        		"menu to appear. Select \"Edit pin name\" from the menu. A box should pop up that will " +
        		"allow you to edit the name of the input. Select \"OK\" for the change to take effect.\n";
        String enableI = "To enable or disable an input, long-press on the item which will cause a context " +
        		"menu to appear. Select \"Disable/Enable pin\" from the menu. If the pin was initially " +
        		"enabled, it will be disabled and appear greyed out in the list; If the pin was initially " +
        		"disabled, it will no longer appear greyed out in the list.\n";
        String change = "You can change the state of a control from the Controls page. In order to do so, " +
        		"click on the toggle button that appears next to the control of interest. Depending on " +
        		"whether you have confirmations enabled in your application settings, a dialog box may " +
        		"appear asking you to confirm the state change; in this case, select \"OK\" to confirm or " +
        		"\"Cancel\" to cancel the change.\n";
        String editO = "To edit the name of an output, long-press on the item which will cause a context " +
        		"menu to appear. Select \"Edit pin name\" from the menu. A box should pop up that will allow " +
        		"you to edit the name of the input. Select \"OK\" for the change to take effect.\n";
        String enableO = "To enable or disable an output, long-press on the item which will cause a context " +
        		"menu to appear. Select \"Disable/Enable pin\" from the menu. If the pin was initially " +
        		"enabled, it will be disabled and appear greyed out in the list; If the pin was initially " +
        		"disabled, it will no longer appear greyed out in the list. Disabling an output will " +
        		"disable the ability to change the state of that particular output.\n";
        String editS = "From the Settings page, select the list item titled \"Server Name\" in order to " +
        		"edit the alias for the server your are using. Select the list item titled \"Server URL\"" +
        		" to edit the URL for the server you would like to use and select \"Server Port\" to " +
        		"specify which port you will be using.\n";
        String enableH = "Check the box for the list item titled \"Use HTTPS\" to indicate that your server " +
        		"uses HTTPS.\n";
        String editC = "Select the list item titled \"User Name\" to edit the username associated with " +
        		"the server connection and select \"Password\" to edit the password associated with the " +
        		"server connection.\n";
        String enableC = "Check the box for the list item titled \"Enable Confirmation\" in order to be " +
        		"prompted for a confirmation prior to changing the state of an output on the Outputs page.";


        // updating TextViews with information
        helpIntro.setText(intro);
        checkState.setText(check);
//        enableNotification.setText(enableN);
        changeState.setText(change);
        editIndName.setText(editI);
        enableInd.setText(enableI);
        editOutName.setText(editO);
        enableOut.setText(enableO);
        editServerInfo.setText(editS);
        enableHTTPS.setText(enableH);
        editCredentials.setText(editC);
        enableConfirm.setText(enableC);

    }
}
