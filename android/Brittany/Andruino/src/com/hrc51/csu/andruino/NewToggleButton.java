package com.hrc51.csu.andruino;

import android.content.Context;
import android.util.AttributeSet;
import android.widget.ToggleButton;

public class NewToggleButton extends ToggleButton {
	
	public NewToggleButton(Context context) {
		super(context);
	}

	public NewToggleButton(Context context, AttributeSet attrs) {
		super(context, attrs);
	}
	
	public NewToggleButton(Context context, AttributeSet attrs, int defStyle) {
		super(context, attrs, defStyle);
	}
	
	public void toggle() {
		// overriding toggle method to do nothing so that I can control toggling
	}
}
