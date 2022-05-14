package com.example.haydeencrm;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.os.Bundle;
import android.os.Handler;

public class SplashScreen extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_splash_screen);



        //Delay
        new Handler(getMainLooper()).postDelayed(() ->{
            finish();
            startActivity(new Intent(SplashScreen.this, Login.class));
        },5000);
    }
}