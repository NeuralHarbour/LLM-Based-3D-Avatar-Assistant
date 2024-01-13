using System;
using System.Threading.Tasks;
using System.Net.Http;
using System.Threading;
using System.Text;
using System.Net;
using System.IO;

namespace VoicevoxBridge
{
    internal class VoicevoxEngineAPI : IDisposable
    {
        HttpClient httpClient;
        Uri engineServerURL;
        Logger logger;

        public VoicevoxEngineAPI(string serverURL, Logger logger)
        {
            httpClient = new HttpClient();
            this.engineServerURL = new Uri(serverURL);
            this.logger = logger;
        }

        public async Task<string> AudioQueryAsync(int speaker, string text, CancellationToken cancellationToken = default)
        {
            string url = $"{engineServerURL}audio_query?speaker={speaker}&text={text}";
            logger.Log("request: " + url);

            try
            {
                using (var response = await httpClient.PostAsync(url, null, cancellationToken))
                {
                    if (response.IsSuccessStatusCode)
                    {
                        logger.Log("AudioQuery request success.");
                        var jsonString = await response.Content.ReadAsStringAsync();
                        cancellationToken.ThrowIfCancellationRequested();
                        return jsonString;
                    }
                    else
                    {
                        var message = await response.Content.ReadAsStringAsync();
                        cancellationToken.ThrowIfCancellationRequested();
                        throw new WebException($"AudioQuery request failed. : {(int)response.StatusCode} {response.StatusCode}\n{message}");
                    }
                }
            }
            catch (OperationCanceledException e)
            {
                throw new OperationCanceledException("AudioQuery request is canceled. ", e);
            }
        }

        public async Task<Stream> SynthesisAsync(int speaker, string jsonQuery, CancellationToken cancellationToken = default)
        {
            string url = $"{engineServerURL}synthesis?speaker={speaker}";
            logger.Log("request: " + url);

            using (var request = new HttpRequestMessage(HttpMethod.Post, url))
            {
                request.Content = new StringContent(jsonQuery, Encoding.UTF8, "application/json");
                HttpResponseMessage response = null;

                try
                {
                    response = await httpClient.SendAsync(request, HttpCompletionOption.ResponseHeadersRead, cancellationToken);

                    if (response.IsSuccessStatusCode)
                    {
                        logger.Log("Synthesis request success.");
                        var stream = await response.Content.ReadAsStreamAsync();
                        cancellationToken.ThrowIfCancellationRequested();
                        return stream;
                    }
                    else
                    {
                        var message = await response.Content.ReadAsStringAsync();
                        cancellationToken.ThrowIfCancellationRequested();
                        throw new WebException($"Synthesis request failed. : {(int)response.StatusCode} {response.StatusCode}\n{message}");
                    }
                }
                catch (Exception e)
                {
                    response?.Dispose();

                    if (e is OperationCanceledException)
                    {
                        throw new OperationCanceledException("Synthesis request canceled.", e);
                    }
                    throw;
                }
            }
        }

        public void Dispose()
        {
            httpClient.Dispose();
        }
    }
}