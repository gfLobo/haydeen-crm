package com.example.haydeencrm.ui.main.tables;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.appcompat.app.AppCompatActivity;
import androidx.cardview.widget.CardView;

import android.annotation.SuppressLint;
import android.app.Dialog;
import android.app.ProgressDialog;
import android.content.Intent;
import android.os.Build;
import android.os.Bundle;
import android.os.Handler;
import android.util.Log;
import android.view.View;
import android.view.ViewGroup;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ImageButton;
import android.widget.ImageView;
import android.widget.Spinner;
import android.widget.Toast;

import com.example.haydeencrm.CreateUserAccountActivity;
import com.example.haydeencrm.HomeActivity;
import com.example.haydeencrm.Login;
import com.example.haydeencrm.R;
import com.example.haydeencrm.SplashScreen;
import com.example.haydeencrm.ui.main.objects.DeleteAccountDialog;
import com.google.android.gms.tasks.Continuation;
import com.google.android.gms.tasks.OnCompleteListener;
import com.google.android.gms.tasks.OnFailureListener;
import com.google.android.gms.tasks.OnSuccessListener;
import com.google.android.gms.tasks.Task;
import com.google.firebase.auth.AuthResult;
import com.google.firebase.auth.FirebaseAuth;
import com.google.firebase.auth.FirebaseUser;
import com.google.firebase.database.DataSnapshot;
import com.google.firebase.database.DatabaseReference;
import com.google.firebase.database.FirebaseDatabase;
import com.google.firebase.firestore.CollectionReference;
import com.google.firebase.firestore.DocumentReference;
import com.google.firebase.firestore.DocumentSnapshot;
import com.google.firebase.firestore.EventListener;
import com.google.firebase.firestore.FirebaseFirestore;
import com.google.firebase.firestore.FirebaseFirestoreException;
import com.google.firebase.firestore.QuerySnapshot;
import com.google.firebase.storage.FirebaseStorage;
import com.google.firebase.storage.StorageReference;

import java.util.ArrayList;
import java.util.Objects;

public class SettingsProfileActivity extends AppCompatActivity implements AdapterView.OnItemSelectedListener,DeleteAccountDialog.DialogDeleteAccListener{

    Spinner spinnerLocal;
    Button btnAtualizarPerfil, btnSair, btnDeletarConta;
    EditText txtNomeEmpresa;
    ImageButton btnBackScreen;

    FirebaseStorage storage = FirebaseStorage.getInstance("gs://crm-vapel.appspot.com");
    StorageReference referenceUsersStorage = storage.getReference("users");
    FirebaseDatabase realTimeDatabaseRef = FirebaseDatabase.getInstance();
    DatabaseReference locaisRealtimeRef = realTimeDatabaseRef.getReferenceFromUrl("https://crm-vapel-default-rtdb.firebaseio.com/");

    FirebaseAuth fAuth = FirebaseAuth.getInstance();
    String userID = Objects.requireNonNull(fAuth.getCurrentUser()).getUid().substring(15);

    FirebaseFirestore db = FirebaseFirestore.getInstance();
    DocumentReference refMatrizFirestore = db.collection("users")
            .document(userID)
            .collection("info").document(userID);
    CollectionReference refUsersFirestoreCollection = db.collection("users");

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_settings_profile);



        spinnerLocal = findViewById(R.id.spinner);
        txtNomeEmpresa = findViewById(R.id.tv_NomeEmpresa);
        btnAtualizarPerfil = findViewById(R.id.btn_RefreshProfile);
        btnBackScreen = findViewById(R.id.backScreen);
        btnSair = findViewById(R.id.btnSair);
        btnDeletarConta = findViewById(R.id.btnDeletAcc);

        spinnerLocal.setBackgroundResource(R.drawable.spinnerlocal);

        spinnerLocal.setOnItemSelectedListener(SettingsProfileActivity.this);


        ProgressDialog dialog = new ProgressDialog(SettingsProfileActivity.this);
        dialog.setMessage("Aguarde...");
        dialog.show();



        //Buttons
        btnAtualizarPerfil.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                if (spinnerLocal.getSelectedItemPosition() !=0 && txtNomeEmpresa.getText().length() !=0) {

                    refMatrizFirestore
                            .update("matriz",txtNomeEmpresa.getText().toString(),
                                    "local",spinnerLocal.getSelectedItem().toString()).addOnSuccessListener(new OnSuccessListener<Void>() {
                        @Override
                        public void onSuccess(Void unused) {
                            Toast.makeText(SettingsProfileActivity.this,
                                    "Perfil Atualizado com sucesso!", Toast.LENGTH_LONG).show();



                            new Handler(getMainLooper()).postDelayed(
                                    SettingsProfileActivity.this::finish,
                                    3000);
                        }
                    }).addOnFailureListener(new OnFailureListener() {
                        @Override
                        public void onFailure(@NonNull Exception e) {
                            Toast.makeText(SettingsProfileActivity.this,
                                    "Um erro ocorreu durante a atualização.", Toast.LENGTH_LONG).show();
                        }
                    });

                }else{
                    Toast.makeText(SettingsProfileActivity.this,
                            "Erro. Preencha corretamente os campos.", Toast.LENGTH_LONG).show();
                }

            }
        });
        btnBackScreen.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                finish();
            }
        });
        btnSair.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {

                new Handler(getMainLooper()).postDelayed(() ->{

                    fAuth.signOut();
                    finish();

                },3000);
                startActivity(new Intent(SettingsProfileActivity.this, Login.class));

            }
        });


        btnDeletarConta.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {

                openDeleteAccountDialog();

            }
        });







        //Autosets
        refMatrizFirestore.addSnapshotListener(new EventListener<DocumentSnapshot>() {
            @Override
            public void onEvent(@Nullable DocumentSnapshot value, @Nullable FirebaseFirestoreException error) {
                assert value != null;
                txtNomeEmpresa.setText(Objects.requireNonNull(Objects.requireNonNull(value.getData()).get("matriz")).toString());
            }
        });
        locaisRealtimeRef.get().addOnSuccessListener(new OnSuccessListener<DataSnapshot>() {
            @Override
            public void onSuccess(DataSnapshot dataSnapshot) {


                ArrayList<String> spinnerList = new ArrayList<>();
                spinnerList.add("UF - Município");
                spinnerList.add("--------------");


                for (  DataSnapshot data : dataSnapshot.getChildren()  ) {


                    spinnerList.add(Objects.requireNonNull(data.child("UF").getValue()) + " - " + Objects.requireNonNull(data.child("Municipio").getValue()));


                }
                dialog.dismiss();

                ArrayAdapter<String> spinnerAdapter = new ArrayAdapter<>(SettingsProfileActivity.this,
                        R.layout.dropdowncustom, spinnerList);


                spinnerLocal.setAdapter(spinnerAdapter);


            }
        });
    }

    private void openDeleteAccountDialog() {

        DeleteAccountDialog deleteAccountDialog = new DeleteAccountDialog();
        deleteAccountDialog.show(getSupportFragmentManager(), "deleteAccountDialog");

    }


    @Override
    public void onItemSelected(AdapterView<?> parent, View view, int position, long id) {

        if (spinnerLocal.getSelectedItemPosition() ==1){
            spinnerLocal.setSelection(0);
        }

    }

    @Override
    public void onNothingSelected(AdapterView<?> parent) {



    }

    @Override
    public void resultDeleteAcc(@NonNull String password) {



        //Login before delete the user auth is required in Firebase
        fAuth.signInWithEmailAndPassword(
                        Objects.requireNonNull(Objects.requireNonNull(fAuth.getCurrentUser()).getEmail()), password
                ).addOnSuccessListener(new OnSuccessListener<AuthResult>() {


                    @Override
                    public void onSuccess(AuthResult authResult) {


                        //Delete Docs

                        /*
                        * Well idk how to do this. I already try the .delete() method but that shit dont works.
                        * f*** off google fix that '-' this is a stupid error or whatever is the method for delete a simple document
                        * */

                        //Delete Logo
                        referenceUsersStorage.child(userID + "/" + "logo").delete();

                        //Delete User Authentication
                        fAuth.getCurrentUser().delete().addOnSuccessListener(new OnSuccessListener<Void>() {
                            @Override
                            public void onSuccess(Void unused) {



                                    try {
                                        //Disable the Local token and finish
                                        fAuth.signOut();
                                        finish();

                                    }catch (Exception e){
                                        Toast.makeText(SettingsProfileActivity.this,
                                                e.getMessage(), Toast.LENGTH_LONG).show();
                                    }

                            }
                        });
                    }
                }).addOnFailureListener(new OnFailureListener() {
            @Override
            public void onFailure(@NonNull Exception e) {
                Toast.makeText(SettingsProfileActivity.this,
                        e.getMessage(), Toast.LENGTH_LONG).show();
            }
        });

    }
}