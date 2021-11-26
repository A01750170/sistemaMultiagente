using System.Collections;
using System.Collections.Generic;
using UnityEditor;
using UnityEngine;
using UnityEngine.Networking;
using Newtonsoft.Json;
public class WebClient : MonoBehaviour
{
    public GameObject carro1;
    public GameObject colliderC1;
    public GameObject carro2;
    public GameObject colliderC2;
    public GameObject carro3;
    public GameObject colliderC3;
    public GameObject carro4;
    public GameObject colliderC4;
    public GameObject carro5;
    public GameObject colliderC5;
    public GameObject carro6;
    public GameObject colliderC6;
    private List<int> semaforos;
    private int contador;
    private Vector3 carro1Pos;
    private Vector3 carro2Pos;
    private Vector3 carro3Pos;
    private Vector3 carro4Pos;
    private Vector3 carro5Pos;
    private Vector3 carro6Pos;
    private Posiciones posCarros;


    // IEnumerator - yield return
    IEnumerator getDataCarro()
    {
        string url = "localhost:8080/carro";
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

                Dictionary<string, List<Dictionary<string,float>>> pos = JsonConvert.DeserializeObject<Dictionary<string, List<Dictionary<string,float>>>>(www.downloadHandler.text);

                // Se actualiza la posición del carro 1
                carro1.transform.position += new Vector3(pos["positions"][0]["x"],pos["positions"][0]["y"],pos["positions"][0]["z"]);
                colliderC1.transform.position += new Vector3(pos["positions"][0]["x"],pos["positions"][0]["y"],pos["positions"][0]["z"]);
                

                // Se actualiza la posición del carro 2
                
                carro2.transform.position += new Vector3(pos["positions"][1]["x"],pos["positions"][1]["y"],pos["positions"][1]["z"]);
                colliderC2.transform.position += new Vector3(pos["positions"][1]["x"],pos["positions"][1]["y"],pos["positions"][1]["z"]);
                

                // Se actualiza la posición del carro 3
                
                carro3.transform.position += new Vector3(pos["positions"][2]["x"],pos["positions"][2]["y"],pos["positions"][2]["z"]);
                colliderC3.transform.position += new Vector3(pos["positions"][2]["x"],pos["positions"][2]["y"],pos["positions"][2]["z"]);
                

                // Se actualiza la posición del carro 4
                
                carro4.transform.position += new Vector3(pos["positions"][3]["x"],pos["positions"][3]["y"],pos["positions"][3]["z"]);
                colliderC4.transform.position += new Vector3(pos["positions"][3]["x"],pos["positions"][3]["y"],pos["positions"][3]["z"]);
                
                // Se actualiza la posición del carro 5
                
                carro5.transform.position += new Vector3(pos["positions"][4]["x"],pos["positions"][4]["y"],pos["positions"][4]["z"]);
                colliderC5.transform.position += new Vector3(pos["positions"][4]["x"],pos["positions"][4]["y"],pos["positions"][4]["z"]);
                

                // Se actualiza la posición del carro 6
                
                carro6.transform.position += new Vector3(pos["positions"][5]["x"],pos["positions"][5]["y"],pos["positions"][5]["z"]);
                colliderC6.transform.position += new Vector3(pos["positions"][5]["x"],pos["positions"][5]["y"],pos["positions"][5]["z"]);
           


            }
        }

    }

    // Start is called before the first frame update
    void Start()
    {
        //string call = "What's up?";
        //Vector3 fakePos = new Vector3(3.44f, 0, -15.707f);
        //string json = EditorJsonUtility.ToJson(fakePos);
        //StartCoroutine(SendData(call));
        //StartCoroutine(getDataSemaforo());
        //StartCoroutine(getDataCarro());
        //transform.localPosition
        contador = 0;
        carro4.transform.position = new Vector3(1973,186,1118);
        
        Posiciones.carro1 = carro1.transform.position;
        Posiciones.carro2 = carro2.transform.position;
        Posiciones.carro3 = carro3.transform.position;
        Posiciones.carro4 = carro4.transform.position;
        Posiciones.carro5 = carro5.transform.position;
        Posiciones.carro6 = carro6.transform.position;
        
    }

    // Update is called once per frame
    void Update()
    {
        if (contador == 10){
            StartCoroutine(getDataCarro());
            contador = 0;
        }
        else{
            contador += 1;
        }
        //StartCoroutine(getDataSemaforo());
        
    }
}
