package com.example.haydeencrm.ui.main;

import androidx.appcompat.app.AppCompatActivity;

import android.annotation.SuppressLint;
import android.os.Bundle;
import android.view.View;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import android.widget.ImageButton;

import com.example.haydeencrm.R;

public class HelperFabActivity extends AppCompatActivity {


    WebView helperWeb;
    ImageButton backHomebtn;

    @SuppressLint("SetJavaScriptEnabled")
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_helper_fab);

        helperWeb = findViewById(R.id.helperWebHaydeen);
        backHomebtn = findViewById(R.id.btnBackHome);

        helperWeb.setWebViewClient(new WebViewClient());
        helperWeb.getSettings().setJavaScriptEnabled(true);
        helperWeb.getSettings().setDomStorageEnabled(true);

        helperWeb.loadUrl("https://gflobo.github.io/haydeen-crm/");







        backHomebtn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                finish();
            }
        });



    }
}