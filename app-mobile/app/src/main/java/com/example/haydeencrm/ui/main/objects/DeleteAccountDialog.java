package com.example.haydeencrm.ui.main.objects;

import android.app.AlertDialog;
import android.app.Dialog;
import android.content.Context;
import android.content.DialogInterface;
import android.content.Intent;
import android.os.Bundle;
import android.os.Handler;
import android.text.Layout;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.widget.EditText;
import android.widget.Toast;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.appcompat.app.AppCompatDialogFragment;

import com.example.haydeencrm.R;
import com.example.haydeencrm.SplashScreen;
import com.example.haydeencrm.ui.main.tables.SettingsProfileActivity;

import java.util.Objects;

public class DeleteAccountDialog extends AppCompatDialogFragment {
    EditText passwordDelete;
    DialogDeleteAccListener dialogDeleteAccListener;



    @NonNull
    @Override
    public Dialog onCreateDialog(@Nullable Bundle savedInstanceState) {
        AlertDialog.Builder builder = new AlertDialog.Builder(getActivity());
        LayoutInflater inflater = requireActivity().getLayoutInflater();
        View view = inflater.inflate(R.layout.popuppasswordtodeleteuser, null);

        builder.setView(view).setTitle("").setNegativeButton("Cancelar", new DialogInterface.OnClickListener() {
            @Override
            public void onClick(DialogInterface dialog, int which) {

            }
        }).setPositiveButton("Deletar", new DialogInterface.OnClickListener() {
            @Override
            public void onClick(DialogInterface dialog, int which) {

                String passwordUser = passwordDelete.getText().toString();
                dialogDeleteAccListener.resultDeleteAcc(passwordUser);
            }
        });
        passwordDelete = view.findViewById(R.id.et_PasswordToDelete);

        return builder.create();

    }


    @Override
    public void onAttach(@NonNull Context context) {
        super.onAttach(context);

        try {
            dialogDeleteAccListener = (DialogDeleteAccListener) context;
        } catch (ClassCastException e) {
            throw new ClassCastException(context +
                    "Deve implementar dialoglistener");
        }
    }

    public interface DialogDeleteAccListener{
        void resultDeleteAcc(String password);
    }
}
