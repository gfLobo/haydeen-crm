package com.example.haydeencrm.ui.main.objects;


public class Filial {

    int id;
    String nomeFilial, localFilial;


    public Filial(int id, String nomeFilial, String localFilial) {
        this.id = id;
        this.nomeFilial = nomeFilial;
        this.localFilial = localFilial;
    }




    public Filial(){

    }




    public int getId() {
        return id;
    }

    public void setId(int id) {
        this.id = id;
    }

    public String getNomeFilial() {
        return nomeFilial;
    }

    public void setNomeFilial(String nomeFilial) {
        this.nomeFilial = nomeFilial;
    }

    public String getLocalFilial() {
        return localFilial;
    }

    public void setLocalFilial(String localFilial) {
        this.localFilial = localFilial;
    }
}
