package com.example.haydeencrm.ui.main.tables;

import androidx.annotation.Nullable;
import androidx.appcompat.app.AppCompatActivity;

import android.os.Bundle;
import android.widget.TextView;

import com.example.haydeencrm.R;
import com.google.firebase.auth.FirebaseAuth;
import com.google.firebase.firestore.CollectionReference;
import com.google.firebase.firestore.DocumentReference;
import com.google.firebase.firestore.DocumentSnapshot;
import com.google.firebase.firestore.EventListener;
import com.google.firebase.firestore.FirebaseFirestore;
import com.google.firebase.firestore.FirebaseFirestoreException;
import com.google.firebase.storage.StorageReference;

import java.text.MessageFormat;
import java.util.Objects;

public class TableChartLinesActivity extends AppCompatActivity {


    FirebaseAuth fAuth = FirebaseAuth.getInstance();

    String userID = Objects.requireNonNull(fAuth.getCurrentUser()).getUid().substring(15);

    FirebaseFirestore db = FirebaseFirestore.getInstance();
    DocumentReference refFatFirestore = db.collection("users")
            .document(userID)
            .collection("faturamento").document(userID);

    TextView txtJan, txtFev, txtMar,txtAbr, txtMai, txtJun,txtJul, txtAgo, txtSet, txtOut, txtNov , txtDez;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_table_chart_lines);

        txtJan = findViewById(R.id.ValueJan);
        txtFev = findViewById(R.id.ValueFev);
        txtMar = findViewById(R.id.ValueMar);
        txtAbr = findViewById(R.id.ValueAbr);
        txtMai = findViewById(R.id.ValueMai);
        txtJun = findViewById(R.id.ValueJun);
        txtJul = findViewById(R.id.ValueJul);
        txtAgo = findViewById(R.id.ValueAgo);
        txtSet = findViewById(R.id.ValueSet);
        txtOut = findViewById(R.id.ValueOut);
        txtNov = findViewById(R.id.ValueNov);
        txtDez = findViewById(R.id.ValueDez);


        refFatFirestore.addSnapshotListener(new EventListener<DocumentSnapshot>() {
            @Override
            public void onEvent(@Nullable DocumentSnapshot value, @Nullable FirebaseFirestoreException error) {
                assert value != null;

                txtJan.setText(MessageFormat.format("R${0}", value.getData().get("jan").toString()));
                txtFev.setText(MessageFormat.format("R${0}",value.getData().get("fev").toString()));
                txtMar.setText(MessageFormat.format("R${0}",value.getData().get("mar").toString()));
                txtAbr.setText(MessageFormat.format("R${0}",value.getData().get("abr").toString()));
                txtMai.setText(MessageFormat.format("R${0}",value.getData().get("mai").toString()));
                txtJun.setText(MessageFormat.format("R${0}",value.getData().get("jun").toString()));
                txtJul.setText(MessageFormat.format("R${0}",value.getData().get("jul").toString()));
                txtAgo.setText(MessageFormat.format("R${0}",value.getData().get("ago").toString()));
                txtSet.setText(MessageFormat.format("R${0}",value.getData().get("set").toString()));
                txtOut.setText(MessageFormat.format("R${0}",value.getData().get("out").toString()));
                txtNov.setText(MessageFormat.format("R${0}",value.getData().get("nov").toString()));
                txtDez.setText(MessageFormat.format("R${0}",value.getData().get("dez").toString()));

            }
        });



    }
}