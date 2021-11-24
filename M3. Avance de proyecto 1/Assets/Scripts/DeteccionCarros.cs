using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Networking;
using Newtonsoft.Json;
public class DeteccionCarros : MonoBehaviour
{
    
    public struct datosCarro{
        public int carro;
        public int estado;
    }
    public int carro;
    datosCarro datos;
    IEnumerator postDataCarro(int estado)
    {
        datos.carro = carro;
        datos.estado = estado;
        string url = "http://localhost:8080/carro";
        string json = JsonUtility.ToJson(datos);
        var request = new UnityWebRequest(url,"POST");
        byte[] jsonToSend = new System.Text.UTF8Encoding().GetBytes(json);
        request.uploadHandler = (UploadHandler)new UploadHandlerRaw(jsonToSend);
        request.downloadHandler = (DownloadHandler)new DownloadHandlerBuffer();
        request.SetRequestHeader("Content-Type", "application/json");
        print("--------------------------------");
        print("Etrné");
        print("--------------------------------");
        yield return request.SendWebRequest();
        
        print(request.downloadHandler.text);
        if (request.downloadHandler.text == "Done"){
            print("DESBONK");
        }else{
            print("ROMANCITO AYUDANOS POR FAOVR");
        }
    }

    IEnumerator postDataSemaforo(int estado)
    {
        datos.carro = carro;
        datos.estado = estado;
        string url = "http://localhost:8080/carro";
        string json = JsonUtility.ToJson(datos);
        var request = new UnityWebRequest(url,"POST");
        byte[] jsonToSend = new System.Text.UTF8Encoding().GetBytes(json);
        request.uploadHandler = (UploadHandler)new UploadHandlerRaw(jsonToSend);
        request.downloadHandler = (DownloadHandler)new DownloadHandlerBuffer();
        request.SetRequestHeader("Content-Type", "application/json");
        print("--------------------------------");
        print("Etrné");
        print("--------------------------------");
        yield return request.SendWebRequest();
        
        print(request.downloadHandler.text);
        if (request.downloadHandler.text == "Done"){
            print("DESBONK");
        }else{
            print("ROMANCITO AYUDANOS POR FAOVR");
        }
    }

    void OnTriggerEnter(Collider other){
        if((other.tag == "CFrente") || (other.tag == "CAtras")){
            StartCoroutine(postDataCarro(0));
        }
        
    }

    void OnTriggerExit(Collider other){
        if((other.tag == "CFrente") || (other.tag == "CAtras")){
            StartCoroutine(postDataCarro(1));
        }
        
    }
}