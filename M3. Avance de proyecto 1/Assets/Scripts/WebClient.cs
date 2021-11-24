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

    // IEnumerator - yield return
    IEnumerator GetDATA()
    {
        string url = "http://localhost:8080/carro";
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
                //Debug.Log(www.downloadHandler.text);    // Answer from Python
                //Vector3 tPos = JsonUtility.FromJson<Vector3>(www.downloadHandler.text.Replace('\'', '\"'));
                //Debug.Log("Form upload complete!");
                //Debug.Log(tPos);
                //string json = JsonConvert.SerializeObject(www.downloadHandler.text);
                Dictionary<string, List<Dictionary<string,int>>> pos = JsonConvert.DeserializeObject<Dictionary<string, List<Dictionary<string,int>>>>(www.downloadHandler.text);
                //Debug.Log("X");
                //Debug.Log(pos["positions"][1]["x"]);
                //Debug.Log("Y");
                //Debug.Log(pos["positions"][1]["y"]);
                //Debug.Log("Z");
                //Debug.Log(pos["positions"][1]["z"]);
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
        StartCoroutine(GetDATA());
        //transform.localPosition
    }

    // Update is called once per frame
    void Update()
    {
        StartCoroutine(GetDATA());
    }
}
