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
    private int rotar;

    void Start(){
        StartCoroutine(getVuelta());
    }

    

    IEnumerator getVuelta()
    {
        string url = "localhost:8080/carroVuelta";
        //string url = "https://trafficandoagentes.us-south.cf.appdomain.cloud/carro";
        using (UnityWebRequest www = UnityWebRequest.Get(url))
        {
            www.downloadHandler = (DownloadHandler)new DownloadHandlerBuffer();
            www.SetRequestHeader("Content-Type", "text/html");
            yield return www.SendWebRequest();          // Talk to Python
            if(www.result == UnityWebRequest.Result.ConnectionError || www.result == UnityWebRequest.Result.ProtocolError)
            {
                Debug.Log(www.error);
            }
            else
            {
                Dictionary<string, List<Dictionary<string,int>>> pos = JsonConvert.DeserializeObject<Dictionary<string, List<Dictionary<string,int>>>>(www.downloadHandler.text);
                // Se actualiza la posición del carro 1
                this.rotar = pos["configVueltas"][carro]["vuelta"];
              
            }
        }
    }

    IEnumerator postDarVuelta()
    {
        string url = "localhost:8080/darVuelta";
        //string url = "https://trafficandoagentes.us-south.cf.appdomain.cloud/carro";
        datosCarro datos;
        datos.carro = carro;
        datos.estado = 0;
        //string url = "https://trafficandoagentes.us-south.cf.appdomain.cloud/carro";
        string json = JsonUtility.ToJson(datos);
        var request = new UnityWebRequest(url,"POST");
        byte[] jsonToSend = new System.Text.UTF8Encoding().GetBytes(json);
        request.uploadHandler = (UploadHandler)new UploadHandlerRaw(jsonToSend);
        request.downloadHandler = (DownloadHandler)new DownloadHandlerBuffer();
        request.SetRequestHeader("Content-Type", "application/json");
        yield return request.SendWebRequest();

        
    }

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
        public int carro;
    }

    IEnumerator postDataSemaforo(int semaforo, bool entrada)
    {
        datosSemafoto datos;
        string url;
        datos.semaforo = semaforo;
        datos.cruza = 1;
        datos.carro = carro;
        string json = JsonUtility.ToJson(datos);
        if(entrada){
            //url = "https://trafficandoagentes.us-south.cf.appdomain.cloud/semaforoEntrada";
            url = "localhost:8080/semaforoEntrada";
        }
        else{
            //url = "https://trafficandoagentes.us-south.cf.appdomain.cloud/semaforoSalida";
            url = "localhost:8080/semaforoSalida";
        }
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
            print("Frenando");
            StartCoroutine(postDataCarro(0));
        }
        if(this.tag == "CFrente" && other.tag == "SEntrada" && rotar == 0){
            StartCoroutine(postDataSemaforo(semaforo, true));
        }
        if(this.tag == "CFrente" && other.tag == "SSalida" && rotar == 0){
            StartCoroutine(postDataSemaforo(semaforo, false));
        }
        if(this.tag == "CFrente" && other.tag == "Vuelta" && rotar == 1){
            float degrees = 90;
            Vector3 to = new Vector3(0, degrees, 0);
            transform.eulerAngles = Vector3.Lerp(transform.rotation.eulerAngles, to, Time.deltaTime);
            StartCoroutine(postDarVuelta());
            //}
        }
        
    }

    void OnTriggerExit(Collider other){
        if((other.tag == "CFrente") || (other.tag == "CAtras")){
            StartCoroutine(postDataCarro(1));
        }
        
    }
}