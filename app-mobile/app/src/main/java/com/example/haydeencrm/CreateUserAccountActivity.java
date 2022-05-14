package com.example.haydeencrm;

import androidx.activity.result.ActivityResultCallback;
import androidx.activity.result.ActivityResultLauncher;
import androidx.activity.result.contract.ActivityResultContracts;
import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;
import androidx.cardview.widget.CardView;

import android.app.ProgressDialog;
import android.content.Intent;
import android.net.Uri;
import android.os.Bundle;
import android.os.Handler;
import android.util.Log;
import android.view.MotionEvent;
import android.view.View;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.EditText;
import android.widget.HorizontalScrollView;
import android.widget.ImageButton;
import android.widget.ImageView;
import android.widget.Spinner;
import android.widget.Toast;

import com.google.android.gms.tasks.OnCompleteListener;
import com.google.android.gms.tasks.OnSuccessListener;
import com.google.android.gms.tasks.Task;
import com.google.firebase.auth.AuthResult;
import com.google.firebase.auth.FirebaseAuth;
import com.google.firebase.database.DataSnapshot;
import com.google.firebase.database.DatabaseReference;
import com.google.firebase.database.FirebaseDatabase;
import com.google.firebase.firestore.CollectionReference;
import com.google.firebase.firestore.FirebaseFirestore;
import com.google.firebase.storage.FirebaseStorage;
import com.google.firebase.storage.StorageReference;

import java.text.MessageFormat;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Locale;
import java.util.Map;
import java.util.Objects;

public class CreateUserAccountActivity extends AppCompatActivity implements AdapterView.OnItemSelectedListener{

    CardView cardView;
    HorizontalScrollView scrollViewSteps;

    EditText emailNewUser, passwordNewUser, confirmPasswordNewUser, empresaNome;
    Button nextStep, backStep, btnCreateNewUserAccount;

    ImageButton backToLogin;
    ImageView  createPic;
    Uri imageUri;
    Spinner spinnerLocalCA;



    FirebaseFirestore db = FirebaseFirestore.getInstance();
    FirebaseAuth fAuth;
    FirebaseStorage storage;
    StorageReference referenceUsersStorage;
    CollectionReference refUsersFirestoreCollection = db.collection("users");
    FirebaseDatabase realTimeDatabaseRef = FirebaseDatabase.getInstance();
    DatabaseReference locaisRealtimeRef = realTimeDatabaseRef.getReferenceFromUrl("https://crm-vapel-default-rtdb.firebaseio.com/");


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_create_user_account);

        cardView = findViewById(R.id.cv_ProfilePic);
        scrollViewSteps = findViewById(R.id.scrollSteps);

        nextStep = findViewById(R.id.btnNextCA);
        backStep = findViewById(R.id.btnVoltarEtapaCA);
        backToLogin = findViewById(R.id.btn_CALoginBack);

        createPic = findViewById(R.id.iv_CAProfilePicture);

        spinnerLocalCA = findViewById(R.id.spinnerCreateAccount);

        btnCreateNewUserAccount = findViewById(R.id.btnCadastro);


        fAuth = FirebaseAuth.getInstance();

        storage = FirebaseStorage.getInstance("gs://crm-vapel.appspot.com");
        referenceUsersStorage = storage.getReference("users");

        //EditTexts
        emailNewUser = findViewById(R.id.et_EmailCreate);
        passwordNewUser = findViewById(R.id.et_PasswordCreate);
        confirmPasswordNewUser = findViewById(R.id.confirmPassword);
        empresaNome = findViewById(R.id.et_EmpresaNomeCA);







        //TasksLayout
        scrollViewSteps.setOnTouchListener(new View.OnTouchListener() {
            @Override
            public boolean onTouch(View v, MotionEvent event) {
                return true;
            }
        });
        cardView.setBackgroundResource(R.drawable.round_cv_profile);

        //LocaisSpinner
        spinnerLocalCA.setBackgroundResource(R.drawable.spinnerlocal);
        spinnerLocalCA.setOnItemSelectedListener(CreateUserAccountActivity.this);
        ProgressDialog dialog = new ProgressDialog(CreateUserAccountActivity.this);
        dialog.setMessage("Aguarde...");
        dialog.show();
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

                ArrayAdapter<String> spinnerAdapter = new ArrayAdapter<>(CreateUserAccountActivity.this,
                        R.layout.dropdowncustom, spinnerList);


                spinnerLocalCA.setAdapter(spinnerAdapter);


            }
        });











        //Buttons
        backToLogin.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                finish();
            }
        });

        backStep.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                scrollViewSteps.postDelayed(new Runnable() {
                    @Override
                    public void run() {
                        scrollViewSteps.fullScroll(View.FOCUS_LEFT);
                    }
                }, 200);
            }
        });
        nextStep.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                if (emailNewUser.getText().length() !=0
                        && passwordNewUser.getText().length() >= 6
                    && confirmPasswordNewUser.getText().toString().equals(passwordNewUser.getText().toString())){

                    scrollViewSteps.postDelayed(new Runnable() {
                        @Override
                        public void run() {
                            scrollViewSteps.fullScroll(View.FOCUS_RIGHT);
                        }
                    }, 200);

                }else if (emailNewUser.getText().length() == 0){
                    Toast.makeText(CreateUserAccountActivity.this,
                            "Preencha os campos de e-mail e senha antes de prosseguir.", Toast.LENGTH_LONG).show();


                }else if (!confirmPasswordNewUser.getText().toString().equals(passwordNewUser.getText().toString())){

                    Toast.makeText(CreateUserAccountActivity.this,
                            "Falha na confirmação de senha.", Toast.LENGTH_LONG).show();

                }else{
                    Toast.makeText(CreateUserAccountActivity.this,
                            "A senha deve conter mais que 6 (seis) dígitos.", Toast.LENGTH_LONG).show();
                }


            }
        });
        btnCreateNewUserAccount.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                if (empresaNome.getText().length() != 0 && spinnerLocalCA.getSelectedItemPosition() !=1){
                    fAuth.signOut();
                    fAuth.createUserWithEmailAndPassword( emailNewUser.getText().toString().toLowerCase(Locale.ROOT).trim(), passwordNewUser.getText().toString().toLowerCase(Locale.ROOT).trim() )
                            .addOnCompleteListener(new OnCompleteListener<AuthResult>() {
                                @Override
                                public void onComplete(@NonNull Task<AuthResult> task) {

                                    if (task.isSuccessful()){
                                        fAuth.signInWithEmailAndPassword( emailNewUser.getText().toString(), passwordNewUser.getText().toString() )
                                                .addOnSuccessListener(new OnSuccessListener<AuthResult>() {
                                                    @Override
                                                    public void onSuccess(AuthResult authResult) {

                                                        String userID = Objects.requireNonNull(fAuth.getCurrentUser()).getUid().substring(15);


                                                        //Faturamento
                                                        Map<String, Object> faturamento = new HashMap<>();
                                                        faturamento.put("jan", 0);
                                                        faturamento.put("fev", 0);
                                                        faturamento.put("mar", 0);
                                                        faturamento.put("abr", 0);
                                                        faturamento.put("mai", 0);
                                                        faturamento.put("jun", 0);
                                                        faturamento.put("jul", 0);
                                                        faturamento.put("ago", 0);
                                                        faturamento.put("set", 0);
                                                        faturamento.put("out", 0);
                                                        faturamento.put("nov", 0);
                                                        faturamento.put("dez", 0);


                                                        refUsersFirestoreCollection.document(userID)
                                                                .collection("faturamento").document(userID).set( faturamento );




                                                        //Info
                                                        Map<String, Object> info = new HashMap<>();
                                                        info.put("matriz", empresaNome.getText().toString());
                                                        info.put("local", spinnerLocalCA.getSelectedItem().toString());


                                                        refUsersFirestoreCollection.document(userID)
                                                                .collection("info").document(userID).set( info );









                                                        //Progresso
                                                        Map<String, Object> progresso = new HashMap<>();
                                                        progresso.put("acompanhamento", 0);
                                                        progresso.put("execucao", 0);
                                                        progresso.put("concluido", 0);
                                                        progresso.put("planejamento", 0);
                                                        progresso.put("apresentacao", 0);

                                                        progresso.put("ativos", 0);
                                                        progresso.put("inativos", 0);


                                                        refUsersFirestoreCollection.document(userID)
                                                                .collection("progresso").document(userID).set( progresso );

                                                        //Imagem
                                                        if (imageUri != null){

                                                            StorageReference Sref = referenceUsersStorage.child(userID + "/" + "logo/");
                                                            Sref.putFile(imageUri);
                                                        }


                                                            finish();
                                                    }
                                                });

                                    }

                                    else {

                                        if (Objects.equals(Objects.requireNonNull(task.getException()).getMessage(),
                                                "The email address is already in use by another account.")){

                                            Toast.makeText(CreateUserAccountActivity.this,
                                                    "Esse e-mail já encontra-se cadastrado",
                                                    Toast.LENGTH_LONG).show();

                                        }else{

                                            Toast.makeText(CreateUserAccountActivity.this,
                                                    "Verifique a correta digitação dos campos de e-mail e senha.",
                                                    Toast.LENGTH_LONG).show();

                                        }



                                    }

                                }
                            });

                }
            }
        });


        //ImageProfile
        createPic.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {

                mGetContent.launch("image/*");

            }
        });

    }




    //Acesso Mídia Interna
    ActivityResultLauncher<String> mGetContent = registerForActivityResult(new ActivityResultContracts.GetContent(), new ActivityResultCallback<Uri>() {
        @Override
        public void onActivityResult(Uri result) {

            if (result != null){
                createPic.setImageURI(result);
                imageUri = result;
            }

        }
    });


    @Override
    public void onItemSelected(AdapterView<?> parent, View view, int position, long id) {

        if (spinnerLocalCA.getSelectedItemPosition() ==1){
            spinnerLocalCA.setSelection(0);
        }

    }

    @Override
    public void onNothingSelected(AdapterView<?> parent) {

    }
}
