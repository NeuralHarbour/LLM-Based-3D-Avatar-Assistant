using System.Threading.Tasks;
using System.Threading;
using UnityEngine;

namespace VoicevoxBridge
{
    public class VOICEVOX : MonoBehaviour
    {
        [SerializeField] AudioSource audioSource = null;
        [SerializeField] string voicevoxEngineURL = "http://localhost:50021/";
        [SerializeField] bool enableLog = false;

        VoicevoxPlayer player = null;

        void Awake()
        {
            if (audioSource == null) audioSource = gameObject.AddComponent<AudioSource>();
            player = new VoicevoxPlayer(voicevoxEngineURL, audioSource);
            player.EnableLog = enableLog;
        }

        public async Task<Voice> CreateVoice(int speaker, string text, CancellationToken cancellationToken = default)
        {
            return await player.CreateVoice(speaker, text, cancellationToken);
        }

        public async Task Play(Voice voice, CancellationToken cancellationToken = default, bool autoReleaseVoice = true)
        {
            await player.Play(voice, cancellationToken, autoReleaseVoice);
        }

        public async Task PlayOneShot(int speaker, string text, CancellationToken cancellationToken = default)
        {
            await player.PlayOneShot(speaker, text, cancellationToken);
        }

        void OnDestroy()
        {
            if (player != null) player.Dispose();
        }
    }
}