package com.example.haydeencrm.ui.main.tables;

import androidx.annotation.Nullable;
import androidx.appcompat.app.AppCompatActivity;

import android.graphics.Color;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;

import com.example.haydeencrm.R;
import com.github.mikephil.charting.charts.BarChart;
import com.github.mikephil.charting.components.AxisBase;
import com.github.mikephil.charting.components.Legend;
import com.github.mikephil.charting.components.LegendEntry;
import com.github.mikephil.charting.components.XAxis;
import com.github.mikephil.charting.data.BarData;
import com.github.mikephil.charting.data.BarDataSet;
import com.github.mikephil.charting.data.BarEntry;
import com.github.mikephil.charting.formatter.IAxisValueFormatter;
import com.github.mikephil.charting.formatter.IndexAxisValueFormatter;
import com.github.mikephil.charting.utils.ColorTemplate;
import com.google.firebase.auth.FirebaseAuth;
import com.google.firebase.firestore.DocumentReference;
import com.google.firebase.firestore.DocumentSnapshot;
import com.google.firebase.firestore.EventListener;
import com.google.firebase.firestore.FirebaseFirestore;
import com.google.firebase.firestore.FirebaseFirestoreException;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.Objects;

public class TableChartProgressActivity extends AppCompatActivity {


    Button backHome;
    BarChart PBChart;

    FirebaseAuth fAuth = FirebaseAuth.getInstance();
    String userID = Objects.requireNonNull(fAuth.getCurrentUser()).getUid().substring(15);
    FirebaseFirestore db = FirebaseFirestore.getInstance();
    DocumentReference produtividadeP = db.collection("users")
            .document(userID)
            .collection("progresso").document(userID);

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_table_chart_progress);

        PBChart = findViewById(R.id.BarProgress);






        Legend legend = PBChart.getLegend();
        legend.setTextSize(15);
        legend.setWordWrapEnabled(true);
        LegendEntry legendEntryA = new LegendEntry();
        LegendEntry legendEntryB = new LegendEntry();
        LegendEntry legendEntryC = new LegendEntry();

        LegendEntry legendEntryE = new LegendEntry();

        produtividadeP.addSnapshotListener(new EventListener<DocumentSnapshot>() {
            @Override
            public void onEvent(@Nullable DocumentSnapshot value, @Nullable FirebaseFirestoreException error) {
                ArrayList<BarEntry> entries = new ArrayList<>();

                assert value != null;


                entries.add(new BarEntry(0, new float[]{

                        Float.parseFloat(Objects.requireNonNull(value.getData()).get("planejamento").toString()),
                        Float.parseFloat(Objects.requireNonNull(value.getData()).get("apresentacao").toString()),

                }));

                entries.add(new BarEntry(1, new float[]{

                        Float.parseFloat(Objects.requireNonNull(value.getData()).get("execucao").toString()),
                        Float.parseFloat(Objects.requireNonNull(value.getData()).get("acompanhamento").toString())
                }));


                BarDataSet set = new BarDataSet(entries, "");
                BarData data = new BarData(set);
                PBChart.setData(data);

                set.setValueTextSize(0);


                set.setColors(
                        Color.rgb(48,178,154),
                        Color.rgb(69,105,192),

                        Color.rgb(63,171,243),
                        Color.rgb(217,144,44));
            }
        });


        legendEntryA.label = "Planejamento";
        legendEntryA.formColor = Color.rgb(48,178,154);
        legendEntryB.label = "Apresentação";
        legendEntryB.formColor = Color.rgb(69,105,192);



        legendEntryC.label = "Execução";
        legendEntryC.formColor = Color.rgb(63,171,243);
        legendEntryE.label = "Acompanhamento";
        legendEntryE.formColor = Color.rgb(217,144,44);

        legend.setCustom(Arrays.asList(legendEntryA, legendEntryB, legendEntryC, legendEntryE));
        PBChart.getDescription().setEnabled(false);
        PBChart.animateXY(2000,2000);
        PBChart.getXAxis().setEnabled(false);
        PBChart.getAxisRight().setEnabled(false);
        PBChart.getAxisLeft().setTextSize(15);

        PBChart.getAxisLeft().setGranularity(1);







        backHome = findViewById(R.id.backProgress);

        backHome.setOnClickListener(v -> finish());
    }
}