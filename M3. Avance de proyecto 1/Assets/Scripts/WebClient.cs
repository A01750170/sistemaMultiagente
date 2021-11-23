using System.Collections;
using System.Collections.Generic;
using UnityEditor;
using UnityEngine;
using UnityEngine.Networking;
using Newtonsoft.Json;
public class WebClient : MonoBehaviour
{
    public GameObject carro1;
    public GameObject carro2;
    // IEnumerator - yield return
    IEnumerator GetDATA()
    {
        string url = "http://localhost:8080";
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
                Debug.Log(pos["positions"][0]["x"]);
                carro1.transform.position += new Vector3(pos["positions"][0]["x"],pos["positions"][0]["y"],pos["positions"][0]["z"]);
                //carro2.transform.position = new Vector3(pos["positions"][0]["x"],pos["positions"][0]["y"],pos["positions"][0]["z"]);
                //carro1.transform.position += new Vector3(-1,0,0);
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
