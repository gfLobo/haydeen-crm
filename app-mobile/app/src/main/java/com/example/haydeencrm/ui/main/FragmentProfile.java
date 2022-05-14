package com.example.haydeencrm.ui.main;

import android.app.ProgressDialog;
import android.content.Intent;
import android.graphics.BitmapFactory;
import android.net.Uri;
import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ImageButton;
import android.widget.ImageView;
import android.widget.TextView;
import android.widget.Toast;

import androidx.activity.result.ActivityResultCallback;
import androidx.activity.result.ActivityResultLauncher;
import androidx.activity.result.contract.ActivityResultContracts;
import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.cardview.widget.CardView;
import androidx.fragment.app.Fragment;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;

import com.example.haydeencrm.R;
import com.example.haydeencrm.ui.main.objects.Filial;
import com.example.haydeencrm.ui.main.objects.RvAdapterFilial;
import com.example.haydeencrm.ui.main.tables.SettingsProfileActivity;
import com.google.android.gms.tasks.OnCompleteListener;
import com.google.android.gms.tasks.OnFailureListener;
import com.google.android.gms.tasks.OnSuccessListener;
import com.google.android.gms.tasks.Task;
import com.google.firebase.auth.FirebaseAuth;
import com.google.firebase.firestore.DocumentReference;
import com.google.firebase.firestore.DocumentSnapshot;
import com.google.firebase.firestore.EventListener;
import com.google.firebase.firestore.FirebaseFirestore;
import com.google.firebase.firestore.FirebaseFirestoreException;
import com.google.firebase.firestore.QuerySnapshot;
import com.google.firebase.storage.FileDownloadTask;
import com.google.firebase.storage.FirebaseStorage;
import com.google.firebase.storage.StorageReference;
import com.google.firebase.storage.UploadTask;

import java.io.File;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Objects;


public class FragmentProfile extends Fragment {


    ImageView Profilepic;
    TextView matrizTxt, localMatrizTxt;
    ImageButton btnSettingsProf;
    CardView cvPhotoProfile, cvInfoMatriz;
    Uri imageUri;


    FirebaseStorage storage;
    StorageReference referenceUsersStorage;

    FirebaseAuth fAuth = FirebaseAuth.getInstance();
    String userID = Objects.requireNonNull(fAuth.getCurrentUser()).getUid().substring(15);
    FirebaseFirestore db = FirebaseFirestore.getInstance();
    DocumentReference refMatrizFirestore = db.collection("users")
            .document(userID)
            .collection("info").document(userID);

    RvAdapterFilial rvAdapterFilial;
    RecyclerView recyclerView;

    public View onCreateView(@NonNull LayoutInflater inflater, @Nullable ViewGroup container, @Nullable Bundle savedInstanceState) {
        View view = inflater.inflate(R.layout.fragment_profile, container, false);

        Profilepic = view.findViewById(R.id.profileImage);
        matrizTxt = view.findViewById(R.id.nomeMatriz);
        localMatrizTxt = view.findViewById(R.id.localMatriz);
        recyclerView = view.findViewById(R.id.rv_filiais);
        cvPhotoProfile = view.findViewById(R.id.roundCvProfilePic);
        cvInfoMatriz= view.findViewById(R.id.cvInfoMatriz);
        btnSettingsProf = view.findViewById(R.id.btn_SettingsProfile);



        storage = FirebaseStorage.getInstance("gs://crm-vapel.appspot.com");
        referenceUsersStorage = storage.getReference("users");










        btnSettingsProf.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                startActivity(new Intent(view.getContext(), SettingsProfileActivity.class));
            }
        });



        refMatrizFirestore.collection("filiais").addSnapshotListener(new EventListener<QuerySnapshot>() {

            @Override
            public void onEvent(@Nullable QuerySnapshot value, @Nullable FirebaseFirestoreException error) {

                recyclerView.setHasFixedSize(true);
                recyclerView.setLayoutManager(new LinearLayoutManager(view.getContext()));
                ArrayList<Filial> filialList = new ArrayList<>();
                rvAdapterFilial = new RvAdapterFilial(view.getContext(),filialList);
                recyclerView.setAdapter(rvAdapterFilial);

                if (error != null){


                    return;

                }

                assert value != null;
                for (int i = 0; i < value.getDocuments().size(); i++) {

                    filialList.add(value.getDocuments().get(i).toObject(Filial.class));

                }


            }
        });

        cvPhotoProfile.setBackgroundResource(R.drawable.round_cv_profile);

        cvInfoMatriz.setBackgroundResource(R.drawable.maininfo);





        refMatrizFirestore.addSnapshotListener(new EventListener<DocumentSnapshot>() {
            @Override
            public void onEvent(@Nullable DocumentSnapshot value, @Nullable FirebaseFirestoreException error) {
                assert value != null;

                    float resizeMatriz = 52.5F;
                    for (int i = 0; i < Objects.requireNonNull(value.get("matriz")).toString().length(); i++) {

                        resizeMatriz -= 0.9999999999;
                    }

                    matrizTxt.setTextSize(resizeMatriz);

                matrizTxt.setText(Objects.requireNonNull(value.get("matriz")).toString());
                localMatrizTxt.setText(Objects.requireNonNull(value.get("local")).toString());

            }
        });



        final long ONE_MEGABYTE = 1024 * 1024;
        referenceUsersStorage.child(userID + "/" + "logo/")
                .getBytes(ONE_MEGABYTE).addOnSuccessListener(new OnSuccessListener<byte[]>() {
            @Override
            public void onSuccess(byte[] bytes) {
                Profilepic.setImageBitmap(BitmapFactory.decodeByteArray(bytes, 0, bytes.length));
            }
        });



        Profilepic.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {

                mGetContent.launch("image/*");

            }
        });




        return view;
    }



    private void uploadFBStorage() {

        ProgressDialog dialog = new ProgressDialog(requireView().getContext());
        dialog.setMessage("Carregando...");
        dialog.show();
        try {


            final File localfile = File.createTempFile("logo","");
            referenceUsersStorage.child(userID + "/logo")
                    .getFile(localfile)



                    .addOnSuccessListener(new OnSuccessListener<FileDownloadTask.TaskSnapshot>() {
                @Override
                public void onSuccess(FileDownloadTask.TaskSnapshot taskSnapshot) {
                    referenceUsersStorage.child(userID + "/logo")

                            .delete().addOnSuccessListener(new OnSuccessListener<Void>() {
                        @Override
                        public void onSuccess(Void unused) {

                            StorageReference Sref = referenceUsersStorage.child(userID + "/" + "logo/");
                            Sref.putFile(imageUri).addOnCompleteListener(new OnCompleteListener<UploadTask.TaskSnapshot>() {
                                @Override
                                public void onComplete(@NonNull Task<UploadTask.TaskSnapshot> task) {

                                    if (task.isSuccessful()){

                                        dialog.dismiss();
                                        Toast.makeText(requireView().getContext(),
                                                "Foto de perfil alterada com sucesso!", Toast.LENGTH_LONG).show();

                                    }else{

                                        dialog.dismiss();
                                        Toast.makeText(requireView().getContext(),
                                                Objects.requireNonNull(task.getException()).getMessage(), Toast.LENGTH_LONG).show();

                                    }

                                }
                            });


                        }

                    });

            }
        })





                    .addOnFailureListener(new OnFailureListener() {
                @Override
                public void onFailure(@NonNull Exception e) {

                    StorageReference Sref = referenceUsersStorage.child(userID + "/" + "logo/");
                    Sref.putFile(imageUri).addOnCompleteListener(new OnCompleteListener<UploadTask.TaskSnapshot>() {
                        @Override
                        public void onComplete(@NonNull Task<UploadTask.TaskSnapshot> task) {

                            if (task.isSuccessful()){

                                dialog.dismiss();
                                Toast.makeText(requireView().getContext(),
                                        "Foto de perfil alterada com sucesso!", Toast.LENGTH_LONG).show();

                            }else{

                                dialog.dismiss();
                                Toast.makeText(requireView().getContext(),
                                        Objects.requireNonNull(task.getException()).getMessage(), Toast.LENGTH_LONG).show();

                            }

                        }
                    });
                }

            });

        } catch (IOException e) {

            e.printStackTrace();


        }




    }

    ActivityResultLauncher<String> mGetContent = registerForActivityResult(new ActivityResultContracts.GetContent(), new ActivityResultCallback<Uri>() {
        @Override
        public void onActivityResult(Uri result) {

            if (result != null){
                Profilepic.setImageURI(result);
                imageUri = result;
                uploadFBStorage();
            }

        }
    });


}
