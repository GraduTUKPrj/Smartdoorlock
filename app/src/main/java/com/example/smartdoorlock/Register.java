package com.example.smartdoorlock;

import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;

import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;

import com.google.android.gms.tasks.OnFailureListener;
import com.google.android.gms.tasks.OnSuccessListener;
import com.google.firebase.database.DatabaseReference;
import com.google.firebase.database.FirebaseDatabase;

import java.util.HashMap;

public class Register extends AppCompatActivity {

    EditText edtID, edtPW, edtName;
    Button btnRegister, btnBack;

    private DatabaseReference mDatabase;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.register);

        edtID = findViewById(R.id.edtID);
        edtPW = findViewById(R.id.edtPW);
        edtName = findViewById(R.id.edtName);

        btnRegister = findViewById(R.id.btnRegister);

        mDatabase = FirebaseDatabase.getInstance().getReference();

        btnRegister.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                String getUserName = edtName.getText().toString();
                String getUserPW = edtPW.getText().toString();
                String getUserID = edtID.getText().toString();

                HashMap result = new HashMap<>();
                result.put("ID", getUserID);
                result.put("NAME", getUserName);
                result.put("PW", getUserPW);

                writeNewUser("1", getUserName, getUserID, getUserPW);
            }
        });
    }

    private void writeNewUser(String uid, String userName, String userID, String userPW){
         User user = new User(userName, userID, userPW);

         mDatabase.child("users").child(userID).setValue(user)
                 .addOnSuccessListener(new OnSuccessListener<Void>() {
                     @Override
                     public void onSuccess(Void unused) {
                         Toast.makeText(Register.this, "가입을 완료했습니다.", Toast.LENGTH_SHORT).show();
                     }
                 })
                 .addOnFailureListener(new OnFailureListener() {
                     @Override
                     public void onFailure(@NonNull Exception e) {
                         Toast.makeText(Register.this, "가입을 실패했습니다.", Toast.LENGTH_SHORT).show();
                     }
                 });

    }
}