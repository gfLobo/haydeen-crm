package com.example.haydeencrm.ui.main.listeners;

import android.location.Location;
import android.location.LocationListener;

import androidx.annotation.NonNull;

public class UserLocation implements LocationListener {



    @Override
    public void onLocationChanged(@NonNull Location location) {

    }

    @Override
    public void onProviderEnabled(@NonNull String provider) {
        LocationListener.super.onProviderEnabled(provider);
    }

    @Override
    public void onProviderDisabled(@NonNull String provider) {
        LocationListener.super.onProviderDisabled(provider);
    }
}
