using System.Collections;
using System.Collections.Generic;
using ReadSpeaker;
using UnityEngine;

public class Spchinstance : MonoBehaviour
{
    string msg = "";
    public TTSSpeaker speaker;
    private bool shouldspeak;
    // Start is called before the first frame update
    void Start()
    {
        TTS.Init();
    }


    // Update is called once per frame
    void Update()
    {
        if (shouldspeak) {
            TTS.SayAsync(msg, speaker);
        }
        shouldspeak = false;
    }
    public void ReceiveMessage(string messageContent)
    {
        msg = messageContent;
        shouldspeak = true;
        Debug.Log("MESSAGE RECIEVED IN INSTANCE : "+msg);
    }

}
