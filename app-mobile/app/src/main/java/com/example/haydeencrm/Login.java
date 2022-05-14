package com.example.haydeencrm;

import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;
import androidx.cardview.widget.CardView;

import android.content.Intent;
import android.os.Bundle;
import android.text.TextUtils;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.Toast;


import com.google.android.gms.tasks.OnCompleteListener;
import com.google.android.gms.tasks.OnFailureListener;
import com.google.android.gms.tasks.OnSuccessListener;
import com.google.android.gms.tasks.Task;
import com.google.firebase.auth.AuthResult;
import com.google.firebase.auth.FirebaseAuth;
import com.google.firebase.auth.FirebaseUser;

import java.util.Locale;
import java.util.Objects;

public class Login extends AppCompatActivity {

    private EditText email, password;
    private FirebaseAuth fAuth;
    TextView btnCriarConta, forgotPassword;
    Button login;
    CardView cardLogin;


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_login2);

        email = findViewById(R.id.ed_email);
        password = findViewById(R.id.ed_password);
        login = findViewById(R.id.btn_login);
        forgotPassword = findViewById(R.id.forgotPassword);
        fAuth = FirebaseAuth.getInstance();
        btnCriarConta = findViewById(R.id.createNewAccount);
        cardLogin = findViewById(R.id.cardViewRoundLogin);




        cardLogin.setBackgroundResource(R.drawable.logincard);

        btnCriarConta.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {

                startActivity(new Intent(Login.this, CreateUserAccountActivity.class));

            }
        });




        login.setOnClickListener(new View.OnClickListener() {

            @Override
            public void onClick(View v) {
                String user_email = email.getText().toString().toLowerCase().trim();
                String user_password = password.getText().toString().toLowerCase().trim();

                if (!user_email.isEmpty() && !user_password.isEmpty()){
                    fAuth.signInWithEmailAndPassword(user_email,user_password)
                            .addOnSuccessListener(new OnSuccessListener<AuthResult>() {
                                @Override
                                public void onSuccess(AuthResult authResult) {
                                    startActivity(new Intent(Login.this, HomeActivity.class));
                                }
                            }).addOnFailureListener(new OnFailureListener() {
                        @Override
                        public void onFailure(@NonNull Exception e) {
                            Toast.makeText(Login.this,
                                    e.getMessage(), Toast.LENGTH_LONG).show();
                        }
                    });
                }else{
                    Toast.makeText(Login.this,
                            "Preencha os campos de e-mail e senha.", Toast.LENGTH_LONG).show();
                }
        }

        });



        forgotPassword.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                if (!email.getText().toString().toLowerCase().trim().isEmpty()){
                    fAuth.sendPasswordResetEmail(email.getText().toString().toLowerCase().trim())
                            .addOnSuccessListener(new OnSuccessListener<Void>() {
                                @Override
                                public void onSuccess(Void unused) {
                                    Toast.makeText(Login.this,
                                            "Um e-mail automático de redefinição será enviado em instantes.", Toast.LENGTH_LONG).show();
                                }
                            }).addOnFailureListener(new OnFailureListener() {
                                @Override
                                public void onFailure(@NonNull Exception e) {
                                    Toast.makeText(Login.this,
                                            e.getMessage(), Toast.LENGTH_LONG).show();
                                }
                            });
                }else {
                    Toast.makeText(Login.this,
                            "Preencha o campo de e-mail antes de redefinir a senha.", Toast.LENGTH_LONG).show();

                }
            }
        });


    }
    @Override
    public void onStart() {
        super.onStart();
        // Check if user is signed in (non-null) and update UI accordingly.
        FirebaseUser currentUser = fAuth.getCurrentUser();
        if(currentUser != null){
            startActivity(new Intent(Login.this, HomeActivity.class));
        }
    }

}