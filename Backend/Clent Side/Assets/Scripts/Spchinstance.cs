using System.Collections;
using System.Collections.Generic;
using ReadSpeaker;
using UnityEngine;
using VoicevoxBridge;

public class Spchinstance : MonoBehaviour
{
    [SerializeField] VOICEVOX voicevox;


    public ElevenlabsAPI elevenlabs;


    string msg = "";
    string x = "";
    string final_message = "";
    public TTSSpeaker speaker_en;
    private bool shouldspeak;
    waveform wv;
    int SpeakerId = 3;
    // Start is called before the first frame update
    void Start()
    {
        TTS.Init();
        wv = GameObject.FindGameObjectWithTag("waveform").GetComponent<waveform>();
    }


    // Update is called once per frame
    void Update()
    {

        if (shouldspeak) {
            x = wv.language;
            Debug.Log("LANGUAGE OF TTS : " + x);
            if (x == "en" || x == "te")
            {
                TTS.SayAsync(final_message, speaker_en);
            }
            else if(x == "ja")
            {
                voicevox.PlayOneShot(SpeakerId, final_message);
            }
            else if(x == "zh")
            {
                elevenlabs.GetAudio(msg);
            }
            else if(x == "ru")
            {
                elevenlabs.GetAudio(msg);
            }
            else
            {
                TTS.SayAsync(msg, speaker_en);
            }
        }
        shouldspeak = false;
    }
    public void ReceiveMessage(string messageContent)
    {
        msg = messageContent;
        shouldspeak = true;
        if (msg.StartsWith("AI:"))
        {
            Debug.Log("MESSAGE STARTS WITH AI:");
            final_message = msg.Substring(3).Trim();
        }
        else
        {
            final_message = messageContent;
        }
        Debug.Log("MESSAGE RECIEVED IN INSTANCE : "+final_message);
    }

}
