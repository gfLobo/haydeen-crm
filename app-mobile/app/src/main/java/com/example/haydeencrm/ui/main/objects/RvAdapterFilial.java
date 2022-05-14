package com.example.haydeencrm.ui.main.objects;

import android.content.Context;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.TextView;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.recyclerview.widget.RecyclerView;

import com.example.haydeencrm.R;
import com.google.android.gms.tasks.OnSuccessListener;
import com.google.firebase.firestore.DocumentReference;
import com.google.firebase.firestore.EventListener;
import com.google.firebase.firestore.FirebaseFirestore;
import com.google.firebase.firestore.FirebaseFirestoreException;
import com.google.firebase.firestore.QuerySnapshot;


import java.util.ArrayList;

public class RvAdapterFilial extends RecyclerView.Adapter<RvAdapterFilial.RvViewHolderFilial> {

    Context context;
    public static ArrayList<Filial> filialArrayList;

    public RvAdapterFilial(Context context, ArrayList<Filial> filialArrayList) {
        this.context = context;
        RvAdapterFilial.filialArrayList = filialArrayList;

    }

    @NonNull
    @Override
    public RvAdapterFilial.RvViewHolderFilial onCreateViewHolder(@NonNull ViewGroup parent, int viewType) {

        View v = LayoutInflater.from(context).inflate(R.layout.filialline, parent, false);

        return new RvViewHolderFilial(v);
    }

    @Override
    public void onBindViewHolder(@NonNull RvAdapterFilial.RvViewHolderFilial holder, int position) {


        Filial filial = filialArrayList.get(position);

        holder.filialTxt.setText(filial.nomeFilial);
        holder.localfilialTxt.setText(filial.localFilial);



    }

    @Override
    public int getItemCount() {
        return filialArrayList.size();
    }



    public static class RvViewHolderFilial extends RecyclerView.ViewHolder{
        TextView filialTxt, localfilialTxt;

        public RvViewHolderFilial(@NonNull View itemView) {
            super(itemView);

            filialTxt = itemView.findViewById(R.id.nomeFilial);
            localfilialTxt = itemView.findViewById(R.id.localFilial);


        }

    }
}
