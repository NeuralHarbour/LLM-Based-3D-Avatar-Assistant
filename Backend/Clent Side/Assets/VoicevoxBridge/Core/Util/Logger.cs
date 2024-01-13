using UnityEngine;

namespace VoicevoxBridge
{
    internal class Logger
    {
        public bool enableLog = true;

        public void Log(string text)
        {
            if (enableLog) Debug.Log($"[VOICEVOX] {text}");
        }

        public void LogWarning(string text)
        {
            Debug.LogWarning($"[VOICEVOX] {text}");
        }
    }
}