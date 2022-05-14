package com.example.haydeencrm.ui.main;

import android.content.Intent;
import android.graphics.Color;
import android.os.Bundle;
import android.telephony.TelephonyScanManager;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.widget.Button;
import android.widget.TextView;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.cardview.widget.CardView;
import androidx.fragment.app.Fragment;

import com.example.haydeencrm.R;
import com.example.haydeencrm.ui.main.tables.TableChartLinesActivity;
import com.example.haydeencrm.ui.main.tables.TableChartProgressActivity;
import com.github.mikephil.charting.charts.LineChart;
import com.github.mikephil.charting.charts.PieChart;
import com.github.mikephil.charting.components.AxisBase;
import com.github.mikephil.charting.components.Legend;
import com.github.mikephil.charting.components.XAxis;
import com.github.mikephil.charting.data.Entry;
import com.github.mikephil.charting.data.LineData;
import com.github.mikephil.charting.data.LineDataSet;
import com.github.mikephil.charting.data.PieData;
import com.github.mikephil.charting.data.PieDataSet;
import com.github.mikephil.charting.data.PieEntry;
import com.github.mikephil.charting.formatter.ValueFormatter;
import com.google.android.gms.tasks.OnCompleteListener;
import com.google.android.gms.tasks.Task;
import com.google.firebase.Timestamp;
import com.google.firebase.auth.FirebaseAuth;
import com.google.firebase.firestore.DocumentReference;
import com.google.firebase.firestore.DocumentSnapshot;
import com.google.firebase.firestore.EventListener;
import com.google.firebase.firestore.FirebaseFirestore;
import com.google.firebase.firestore.FirebaseFirestoreException;
import com.google.firebase.firestore.Query;
import com.google.firebase.firestore.core.AsyncEventListener;
import com.google.firebase.firestore.core.SyncEngine;
import com.google.firebase.firestore.model.SnapshotVersion;

import java.text.MessageFormat;
import java.util.ArrayList;
import java.util.List;
import java.util.Objects;
import java.util.concurrent.Executor;

import javax.security.auth.callback.Callback;


public class FragmentDash extends Fragment {
    FirebaseFirestore db = FirebaseFirestore.getInstance();


    LineChart lineChart;
    LineData lineData;

    LineChart lineChart2;
    LineData lineData2;

    PieChart pieChart;







    CardView cVAproveitamento,cvFat,CVclientesAtivos,CVclientesInativos;
    TextView TVCliAtivos,TVCliInativos;
    Button maisPData;



    FirebaseAuth fAuth = FirebaseAuth.getInstance();
    String userID = Objects.requireNonNull(fAuth.getCurrentUser()).getUid().substring(15);

    DocumentReference fat = db.collection("users")
            .document(userID)
            .collection("faturamento").document(userID);

    DocumentReference atvClientes = db.collection("users")
            .document(userID)
            .collection("progresso").document(userID);

    public View onCreateView(LayoutInflater inflater,
                             ViewGroup container,
                             Bundle savedInstanceState) {

        View view = inflater.inflate(R.layout.fragment_dash, container, false);


        cVAproveitamento = view.findViewById(R.id.CVAproveitamento);
        cvFat = view.findViewById(R.id.fatCV);
        CVclientesInativos = view.findViewById(R.id.CVCliInativo);
        CVclientesAtivos = view.findViewById(R.id.CVCLiAtivos);
        TVCliAtivos = view.findViewById(R.id.TVClientesAtivos);
        TVCliInativos = view.findViewById(R.id.TVClientesInativos);
        maisPData = view.findViewById(R.id.btnMaisProgressData);


        cVAproveitamento.setBackgroundResource(R.drawable.mainhomecv);
        cvFat.setBackgroundResource(R.drawable.cardmainbg);
        CVclientesAtivos.setBackgroundResource(R.drawable.atvcard);
        CVclientesInativos.setBackgroundResource(R.drawable.intcard);



        //Charts
        lineChart = view.findViewById(R.id.lineChart);
        lineChart2 = view.findViewById(R.id.lineChart2);
        pieChart = view.findViewById(R.id.pieChart);










        //Atividade de Clientes
        atvClientes.addSnapshotListener(new EventListener<DocumentSnapshot>() {
            @Override
            public void onEvent(@Nullable DocumentSnapshot value, @Nullable FirebaseFirestoreException error) {
                assert value != null;
                float CliAtivos = Float.parseFloat(Objects.requireNonNull(value.get("ativos")).toString());
                float CliInativos = Float.parseFloat(Objects.requireNonNull(value.get("inativos")).toString());





                String setResizeCliAtivos;
                if (CliAtivos>1000 && CliAtivos<1000000){

                    String adapterNum = String.valueOf(CliAtivos / 1000);
                    if ( adapterNum.charAt(adapterNum.length() -1 ) == '0'){

                        setResizeCliAtivos = ((int) CliAtivos / 1000) + "K";

                    }else {

                        setResizeCliAtivos = CliAtivos / 1000 + "K";

                    }

                }else if (CliAtivos>1000000){

                    String adapterNum = String.valueOf(CliAtivos / 1000000);
                    if ( adapterNum.charAt(adapterNum.length() -1 ) == '0'){

                        setResizeCliAtivos = ((int) CliAtivos / 1000000) + "M";

                    }else {

                        setResizeCliAtivos = CliAtivos / 1000000 + "M";

                    }

                }else{

                    setResizeCliAtivos = String.valueOf((int) CliAtivos);

                }

                TVCliAtivos.setText(MessageFormat.format("{0}", setResizeCliAtivos));


                String setResizeCliInativos;
                if (CliInativos > 1000 && CliInativos < 1000000){
                    String adapterNum = String.valueOf(CliInativos / 1000);
                    if ( adapterNum.charAt(adapterNum.length() -1 ) == '0'){

                        setResizeCliInativos = ((int) CliInativos / 1000) + "K";

                    }else {

                        setResizeCliInativos = CliInativos / 1000 + "K";

                    }

                }else if (CliInativos > 1000000){

                    String adapterNum = String.valueOf(CliInativos / 1000000);
                    if ( adapterNum.charAt(adapterNum.length() -1 ) == '0'){

                        setResizeCliInativos = ((int) CliInativos / 1000000) + "M";

                    }else {

                        setResizeCliInativos = CliInativos / 1000000 + "M";

                    }

                }else{

                    setResizeCliInativos = String.valueOf((int) CliInativos);

                }

                TVCliInativos.setText(MessageFormat.format("{0}", setResizeCliInativos));
            }
        });




        //Progresso
        atvClientes.addSnapshotListener(new EventListener<DocumentSnapshot>() {
            @Override
            public void onEvent(@Nullable DocumentSnapshot value, @Nullable FirebaseFirestoreException error) {
                ArrayList<PieEntry> pieEntries = new ArrayList<>();


                assert value != null;


                float Aproveitados = Integer.parseInt(Objects.requireNonNull(value.get("acompanhamento")).toString()) + Integer.parseInt(Objects.requireNonNull(value.get("execucao")).toString());
                float NaoAproveitados =  Integer.parseInt(Objects.requireNonNull(value.get("planejamento")).toString()) + Integer.parseInt(Objects.requireNonNull(value.get("apresentacao")).toString());
                float QtdCompras = Aproveitados + NaoAproveitados;
                int desempenho = Math.round( (Aproveitados / QtdCompras) * 100 );

                pieEntries.add(new PieEntry(Aproveitados,1));
                pieEntries.add(new PieEntry(NaoAproveitados,2));

                PieDataSet pieDataSet = new PieDataSet(pieEntries,"");

                if (desempenho >= 70){

                    pieChart.setCenterText("🤍 " + desempenho + "%");
                    pieDataSet.setColors(Color.WHITE,Color.TRANSPARENT);
                }else if (desempenho >= 50){

                    pieChart.setCenterText("🩹 " + desempenho + "%");
                    pieDataSet.setColors(Color.rgb(217,154,44),Color.TRANSPARENT);

                }else if (desempenho >= 40){

                    pieChart.setCenterText("💢 " + desempenho + "%");
                    pieDataSet.setColors(Color.RED,Color.TRANSPARENT);

                }else {

                    pieChart.setCenterText("🚨 " + desempenho + "%");
                    pieDataSet.setColors(Color.RED,Color.TRANSPARENT);

                }










                pieChart.setData(new PieData(pieDataSet));
                pieChart.setHoleColor(Color.TRANSPARENT);
                pieChart.animateXY(2000,2000);
                pieChart.getLegend().setEnabled(false);
                pieChart.getDescription().setEnabled(false);
                pieDataSet.setDrawValues(false);
                pieChart.setHoleRadius(85);
                pieChart.setCenterTextSize(35);
                pieChart.setCenterTextColor(Color.WHITE);

                pieChart.setHoleColor(Color.TRANSPARENT);
            }
        });









        //Semesters
        fat.addSnapshotListener(new EventListener<DocumentSnapshot>() {
            @Override
            public void onEvent(@Nullable DocumentSnapshot value, @Nullable FirebaseFirestoreException error) {




                //1th Semester
                assert value != null;
                List<Entry> entryList = new ArrayList<>();

                entryList.add(new
                        Entry(0,
                        Float.parseFloat(String.valueOf(Objects.requireNonNull(value.getData()).get("jan")))));
                entryList.add(new
                        Entry(1,
                        Float.parseFloat(String.valueOf(Objects.requireNonNull(value.getData()).get("fev")))));
                entryList.add(new
                        Entry(2,
                        Float.parseFloat(String.valueOf(Objects.requireNonNull(value.getData()).get("mar")))));
                entryList.add(new
                        Entry(3,
                        Float.parseFloat(String.valueOf(Objects.requireNonNull(value.getData()).get("abr")))));
                entryList.add(new
                        Entry(4,
                        Float.parseFloat(String.valueOf(Objects.requireNonNull(value.getData()).get("mai")))));
                entryList.add(new
                        Entry(5,
                        Float.parseFloat(String.valueOf(Objects.requireNonNull(value.getData()).get("jun")))));




                LineDataSet lineDataSet = new LineDataSet(entryList,"");
                XAxis xAxis = lineChart.getXAxis();
                lineData = new LineData(lineDataSet);

                lineDataSet.setColor(Color.rgb(1,135,134));
                lineDataSet.setCircleRadius(5);
                lineDataSet.setLineWidth(2);
                lineDataSet.setDrawFilled(true);
                xAxis.setPosition(XAxis.XAxisPosition.BOTTOM);
                lineDataSet.setCircleHoleRadius(2);
                lineDataSet.setCircleHoleColor(Color.WHITE);
                lineDataSet.setCircleColor(Color.rgb(1,135,134));

                lineChart.setData(lineData);
                lineChart.getLegend().setForm(Legend.LegendForm.NONE);

                lineChart.getAxisRight().setDrawGridLines(false);
                lineChart.getAxisLeft().setDrawGridLines(false);
                lineChart.getXAxis().setDrawGridLines(false);

                lineChart.getDescription().setEnabled(false);
                lineChart.setGridBackgroundColor(Color.TRANSPARENT);
                lineChart.getAxisRight().setDrawLabels(false);
                lineChart.getAxisLeft().setDrawLabels(true);
                lineData.setValueTextSize(0);
                lineChart.getAxisLeft().setTextSize(12);
                lineChart.getAxisLeft().setTextColor(Color.rgb(1,135,134));

                lineChart.setExtraLeftOffset(10);lineChart.setExtraRightOffset(33);
                lineChart.animateXY(2000,2000);
                xAxis.setGranularity(1f);
                xAxis.setGranularityEnabled(true);


                xAxis.setValueFormatter(new ValueFormatter() {
                    @Override
                    public String getAxisLabel(float value, AxisBase axis) {
                        String label = "";

                        if (value ==0){
                            label = "Jan";
                        }else if (value ==1){
                            label = "Fev";
                        }else if (value ==2){
                            label = "Mar";
                        }else if (value ==3){
                            label = "Abr";
                        }else if (value ==4){
                            label = "Mai";
                        }else if (value ==5){
                            label = "Jun";
                        }
                        return label;
                    }

                });
                xAxis.setTextSize(15);
                xAxis.setTextColor(Color.rgb(1,135,134));
            }
        });



        fat.addSnapshotListener(new EventListener<DocumentSnapshot>() {
            @Override
            public void onEvent(@Nullable DocumentSnapshot value, @Nullable FirebaseFirestoreException error) {


                List<Entry> entryList2 = new ArrayList<>();





                entryList2.add(new
                        Entry(0,
                        Float.parseFloat(String.valueOf(Objects.requireNonNull(value.getData()).get("jul")))));
                entryList2.add(new
                        Entry(1,
                        Float.parseFloat(String.valueOf(Objects.requireNonNull(value.getData()).get("ago")))));
                entryList2.add(new
                        Entry(2,
                        Float.parseFloat(String.valueOf(Objects.requireNonNull(value.getData()).get("set")))));
                entryList2.add(new
                        Entry(3,
                        Float.parseFloat(String.valueOf(Objects.requireNonNull(value.getData()).get("out")))));
                entryList2.add(new
                        Entry(4,
                        Float.parseFloat(String.valueOf(Objects.requireNonNull(value.getData()).get("nov")))));
                entryList2.add(new
                        Entry(5,
                        Float.parseFloat(String.valueOf(Objects.requireNonNull(value.getData()).get("dez")))));



                LineDataSet lineDataSet2 = new LineDataSet(entryList2,"");
                XAxis xAxis2 = lineChart2.getXAxis();
                lineData2 = new LineData(lineDataSet2);


                xAxis2.setPosition(XAxis.XAxisPosition.BOTTOM);
                lineDataSet2.setColor(Color.rgb(1,135,134));
                lineDataSet2.setCircleHoleRadius(2);
                lineDataSet2.setCircleRadius(5);
                lineDataSet2.setCircleColor(Color.rgb(1,135,134));
                lineDataSet2.setCircleHoleColor(Color.WHITE);
                lineDataSet2.setLineWidth(2);
                lineDataSet2.setDrawFilled(true);
                lineChart2.setData(lineData2);

                lineChart2.getLegend().setForm(Legend.LegendForm.NONE);
                lineChart2.setBackgroundColor(Color.TRANSPARENT);
                lineChart2.getDescription().setEnabled(false);
                lineChart2.getAxisRight().setDrawLabels(false);
                lineData2.setValueTextSize(0);
                lineChart2.getAxisLeft().setTextSize(12);
                lineChart2.getAxisRight().setDrawGridLines(false);
                lineChart2.getAxisLeft().setDrawGridLines(false);
                lineChart2.getAxisLeft().setTextColor(Color.rgb(1,135,134));

                lineChart2.getXAxis().setDrawGridLines(false);
                lineChart2.setExtraLeftOffset(10);lineChart2.setExtraRightOffset(33);
                lineChart2.animateXY(2000,2000);


                xAxis2.setGranularity(1f);
                xAxis2.setGranularityEnabled(true);







                xAxis2.setValueFormatter(new ValueFormatter() {
                    @Override
                    public String getAxisLabel(float value, AxisBase axis) {
                        String label = "";

                        if (value ==0){
                            label = "Jul";
                        }else if (value ==1){
                            label = "Ago";
                        }else if (value ==2){
                            label = "Set";
                        }else if (value ==3){
                            label = "Out";
                        }else if (value ==4){
                            label = "Nov";
                        }else if (value ==5){
                            label = "Dez";
                        }
                        return label;
                    }
                });
                xAxis2.setTextSize(15);
                xAxis2.setTextColor(Color.rgb(1,135,134));
            }
        });










        //Lines onClickListeners
        lineChart.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {

                startActivity(new Intent(view.getContext(), TableChartLinesActivity.class));

            }
        });

        lineChart2.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {

                startActivity(new Intent(view.getContext(), TableChartLinesActivity.class));


            }
        });






        //Progress onClickListeners
        maisPData.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {

                startActivity(new Intent(view.getContext(), TableChartProgressActivity.class));


            }
        });



        return view;
    }


}
