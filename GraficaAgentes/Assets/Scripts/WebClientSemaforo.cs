using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Networking;
using Newtonsoft.Json;

public class WebClientSemaforo : MonoBehaviour
{
    // Semaforo 0
    public GameObject s0v;
    public GameObject s0a;
    public GameObject s0r;

    // Semaforo 1
    public GameObject s1v;
    public GameObject s1a;
    public GameObject s1r;

    // Semaforo 2
    public GameObject s2v;
    public GameObject s2a;
    public GameObject s2r;

    // Semaforo 3
    public GameObject s3v;
    public GameObject s3a;
    public GameObject s3r;
    private int contador;

    // IEnumerator - yield return
    IEnumerator getDataSemaforo()
    {
        string url = "localhost:8080/semaforo";
        //string url = "https://trafficandoagentes.us-south.cf.appdomain.cloud/carro";
        using (UnityWebRequest www = UnityWebRequest.Get(url))
        {
            //byte[] bodyRaw = System.Text.Encoding.UTF8.GetBytes();
            //www.uploadHandler = (UploadHandler)new UploadHandlerRaw(bodyRaw);
            www.downloadHandler = (DownloadHandler)new DownloadHandlerBuffer();
            www.SetRequestHeader("Content-Type", "text/html");
            //www.SetRequestHeader("Content-Type", "application/json");

            yield return www.SendWebRequest();          // Talk to Python
            if(www.result == UnityWebRequest.Result.ConnectionError || www.result == UnityWebRequest.Result.ProtocolError)
            {
                Debug.Log(www.error);
            }
            else
            {
                
                Dictionary<string, List<Dictionary<string,string>>> pos = JsonConvert.DeserializeObject<Dictionary<string, List<Dictionary<string,string>>>>(www.downloadHandler.text);
                List<Dictionary<string,string>> semaforos = pos["semaforos"];
                // Cambia el color del semaforo 0
                if (semaforos[0]["semaforo"] == "0"){
                    if(semaforos[0]["estado"]=="amarillo"){
                        Material mat1 = s0a.GetComponent<Renderer>().material;
                        mat1.SetColor("_EmissionColor", Color.yellow);
                        mat1.EnableKeyword("_EMISSION");
                        Material mat2 = s0r.GetComponent<Renderer>().material;
                        mat2.SetColor("_EmissionColor", Color.red);
                        mat2.DisableKeyword("_EMISSION");
                        Material mat3 = s0v.GetComponent<Renderer>().material;
                        mat3.SetColor("_EmissionColor", Color.green);
                        mat3.DisableKeyword("_EMISSION");
                    }
                    if(semaforos[0]["estado"]=="rojo"){
                        Material mat1 = s0a.GetComponent<Renderer>().material;
                        mat1.SetColor("_EmissionColor", Color.yellow);
                        mat1.DisableKeyword("_EMISSION");
                        Material mat2 = s0r.GetComponent<Renderer>().material;
                        mat2.SetColor("_EmissionColor", Color.red);
                        mat2.EnableKeyword("_EMISSION");
                        Material mat3 = s0v.GetComponent<Renderer>().material;
                        mat3.SetColor("_EmissionColor", Color.green);
                        mat3.DisableKeyword("_EMISSION");
                    }
                    if(semaforos[0]["estado"]=="verde"){
                        Material mat1 = s0a.GetComponent<Renderer>().material;
                        mat1.SetColor("_EmissionColor", Color.yellow);
                        mat1.DisableKeyword("_EMISSION");
                        Material mat2 = s0r.GetComponent<Renderer>().material;
                        mat2.SetColor("_EmissionColor", Color.red);
                        mat2.DisableKeyword("_EMISSION");
                        Material mat3 = s0v.GetComponent<Renderer>().material;
                        mat3.SetColor("_EmissionColor", Color.green);
                        mat3.EnableKeyword("_EMISSION");
                    }
                }

                // Cambia el color del semaforo 1
                if (semaforos[1]["semaforo"] == "1"){
                    if(semaforos[1]["estado"]=="amarillo"){
                        Material mat1 = s1a.GetComponent<Renderer>().material;
                        mat1.SetColor("_EmissionColor", Color.yellow);
                        mat1.EnableKeyword("_EMISSION");
                        Material mat2 = s1r.GetComponent<Renderer>().material;
                        mat2.SetColor("_EmissionColor", Color.red);
                        mat2.DisableKeyword("_EMISSION");
                        Material mat3 = s1v.GetComponent<Renderer>().material;
                        mat3.SetColor("_EmissionColor", Color.green);
                        mat3.DisableKeyword("_EMISSION");
                    }
                    if(semaforos[1]["estado"]=="rojo"){
                        Material mat1 = s1a.GetComponent<Renderer>().material;
                        mat1.SetColor("_EmissionColor", Color.yellow);
                        mat1.DisableKeyword("_EMISSION");
                        Material mat2 = s1r.GetComponent<Renderer>().material;
                        mat2.SetColor("_EmissionColor", Color.red);
                        mat2.EnableKeyword("_EMISSION");
                        Material mat3 = s1v.GetComponent<Renderer>().material;
                        mat3.SetColor("_EmissionColor", Color.green);
                        mat3.DisableKeyword("_EMISSION");
                    }
                    if(semaforos[1]["estado"]=="verde"){
                        Material mat1 = s1a.GetComponent<Renderer>().material;
                        mat1.SetColor("_EmissionColor", Color.yellow);
                        mat1.DisableKeyword("_EMISSION");
                        Material mat2 = s1r.GetComponent<Renderer>().material;
                        mat2.SetColor("_EmissionColor", Color.red);
                        mat2.DisableKeyword("_EMISSION");
                        Material mat3 = s1v.GetComponent<Renderer>().material;
                        mat3.SetColor("_EmissionColor", Color.green);
                        mat3.EnableKeyword("_EMISSION");
                    }
                }

                // Cambia el color del semaforo 2
                if (semaforos[2]["semaforo"] == "2"){
                    if(semaforos[2]["estado"]=="amarillo"){
                        Material mat1 = s2a.GetComponent<Renderer>().material;
                        mat1.SetColor("_EmissionColor", Color.yellow);
                        mat1.EnableKeyword("_EMISSION");
                        Material mat2 = s2r.GetComponent<Renderer>().material;
                        mat2.SetColor("_EmissionColor", Color.red);
                        mat2.DisableKeyword("_EMISSION");
                        Material mat3 = s2v.GetComponent<Renderer>().material;
                        mat3.SetColor("_EmissionColor", Color.green);
                        mat3.DisableKeyword("_EMISSION");
                    }
                    if(semaforos[2]["estado"]=="rojo"){
                        Material mat1 = s2a.GetComponent<Renderer>().material;
                        mat1.SetColor("_EmissionColor", Color.yellow);
                        mat1.DisableKeyword("_EMISSION");
                        Material mat2 = s2r.GetComponent<Renderer>().material;
                        mat2.SetColor("_EmissionColor", Color.red);
                        mat2.EnableKeyword("_EMISSION");
                        Material mat3 = s2v.GetComponent<Renderer>().material;
                        mat3.SetColor("_EmissionColor", Color.green);
                        mat3.DisableKeyword("_EMISSION");
                    }
                    if(semaforos[2]["estado"]=="verde"){
                        Material mat1 = s2a.GetComponent<Renderer>().material;
                        mat1.SetColor("_EmissionColor", Color.yellow);
                        mat1.DisableKeyword("_EMISSION");
                        Material mat2 = s2r.GetComponent<Renderer>().material;
                        mat2.SetColor("_EmissionColor", Color.red);
                        mat2.DisableKeyword("_EMISSION");
                        Material mat3 = s2v.GetComponent<Renderer>().material;
                        mat3.SetColor("_EmissionColor", Color.green);
                        mat3.EnableKeyword("_EMISSION");
                    }
                }
                // Cambia el color del semaforo 3
                if (semaforos[3]["semaforo"] == "3"){
                    if(semaforos[3]["estado"]=="amarillo"){
                        Material mat1 = s3a.GetComponent<Renderer>().material;
                        mat1.SetColor("_EmissionColor", Color.yellow);
                        mat1.EnableKeyword("_EMISSION");
                        Material mat2 = s3r.GetComponent<Renderer>().material;
                        mat2.SetColor("_EmissionColor", Color.red);
                        mat2.DisableKeyword("_EMISSION");
                        Material mat3 = s3v.GetComponent<Renderer>().material;
                        mat3.SetColor("_EmissionColor", Color.green);
                        mat3.DisableKeyword("_EMISSION");
                    }
                    if(semaforos[3]["estado"]=="rojo"){
                        Material mat1 = s3a.GetComponent<Renderer>().material;
                        mat1.SetColor("_EmissionColor", Color.yellow);
                        mat1.DisableKeyword("_EMISSION");
                        Material mat2 = s3r.GetComponent<Renderer>().material;
                        mat2.SetColor("_EmissionColor", Color.red);
                        mat2.EnableKeyword("_EMISSION");
                        Material mat3 = s3v.GetComponent<Renderer>().material;
                        mat3.SetColor("_EmissionColor", Color.green);
                        mat3.DisableKeyword("_EMISSION");
                    }
                    if(semaforos[3]["estado"]=="verde"){
                        Material mat1 = s3a.GetComponent<Renderer>().material;
                        mat1.SetColor("_EmissionColor", Color.yellow);
                        mat1.DisableKeyword("_EMISSION");
                        Material mat2 = s3r.GetComponent<Renderer>().material;
                        mat2.SetColor("_EmissionColor", Color.red);
                        mat2.DisableKeyword("_EMISSION");
                        Material mat3 = s3v.GetComponent<Renderer>().material;
                        mat3.SetColor("_EmissionColor", Color.green);
                        mat3.EnableKeyword("_EMISSION");
                    }
                }
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
        StartCoroutine(getDataSemaforo());
        //transform.localPosition
        contador = 0;
    }

    // Update is called once per frame
    void Update()
    {
        if (contador == 10){
            StartCoroutine(getDataSemaforo());
            contador = 0;
        }
        else{
            contador += 1;
        }
        //StartCoroutine(getDataSemaforo());
        
    }
}
