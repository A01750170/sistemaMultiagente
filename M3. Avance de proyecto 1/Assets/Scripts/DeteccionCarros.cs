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
    public int semaforo;
    IEnumerator postDataCarro(int estado)
    {
        datosCarro datos;
        datos.carro = carro;
        datos.estado = estado;
        //string url = "https://trafficandoagentes.us-south.cf.appdomain.cloud/carro";
        string url = "localhost:8080/carro";
        string json = JsonUtility.ToJson(datos);
        var request = new UnityWebRequest(url,"POST");
        byte[] jsonToSend = new System.Text.UTF8Encoding().GetBytes(json);
        request.uploadHandler = (UploadHandler)new UploadHandlerRaw(jsonToSend);
        request.downloadHandler = (DownloadHandler)new DownloadHandlerBuffer();
        request.SetRequestHeader("Content-Type", "application/json");
        yield return request.SendWebRequest();
        //print(request.downloadHandler.text);
    }

    public struct datosSemafoto{
        public int semaforo;
        public int cruza;
    }

    IEnumerator postDataSemaforo(int semaforo, bool entrada)
    {
        datosSemafoto datos;
        string url;
        datos.semaforo = semaforo;
        datos.cruza = 1;
        if(entrada){
            //url = "https://trafficandoagentes.us-south.cf.appdomain.cloud/semaforoEntrada";
            url = "localhost:8080/semaforoEntrada";
        }
        else{
            //url = "https://trafficandoagentes.us-south.cf.appdomain.cloud/semaforoSalida";
            url = "localhost:8080/semaforoSalida";
        }
        string json = JsonUtility.ToJson(datos);
        var request = new UnityWebRequest(url,"POST");
        byte[] jsonToSend = new System.Text.UTF8Encoding().GetBytes(json);
        request.uploadHandler = (UploadHandler)new UploadHandlerRaw(jsonToSend);
        request.downloadHandler = (DownloadHandler)new DownloadHandlerBuffer();
        request.SetRequestHeader("Content-Type", "application/json");
        yield return request.SendWebRequest();
        
        //print(request.downloadHandler.text);
        //if (request.downloadHandler.text == "Done"){
            //print($"Soy el camrrito {carro} y pamse el semamforo {semaforo}");
        //}else{
            //print("ROMANCITO AYUDANOS POR FAOVR");
        //}
    }

    void OnTriggerEnter(Collider other){
        if((other.tag == "CFrente") || (other.tag == "CAtras")){
            StartCoroutine(postDataCarro(0));
        }
        if(this.tag == "CFrente" && other.tag == "SEntrada"){
            print($"Soy el camrrito {carro} y pamse el semamforo {semaforo}");
            StartCoroutine(postDataSemaforo(semaforo, true));
        }
        if(this.tag == "CFrente" && other.tag == "SSalida"){
            print($"Soy el camrrito {carro} terminé mi cruce");
            StartCoroutine(postDataSemaforo(semaforo, false));
        }
        
    }

    void OnTriggerExit(Collider other){
        if((other.tag == "CFrente") || (other.tag == "CAtras")){
            StartCoroutine(postDataCarro(1));
        }
        
    }
}