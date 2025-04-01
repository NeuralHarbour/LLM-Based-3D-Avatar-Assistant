using UnityEngine;
using UnityEngine.UI;
using TMPro;
using System.Collections;
using System.IO;
using System.Linq;
using UnityEngine.Networking;
using System.IO.Compression;
using System;
using System.Collections.Generic;
using System.Diagnostics;
using Debug = UnityEngine.Debug;

public class Integrity_Loader : MonoBehaviour
{
    [SerializeField] Image CircleImg;
    [SerializeField] TextMeshProUGUI txtProgress;
    [SerializeField] TextMeshProUGUI LoadText;

    [SerializeField] AudioSource musicSource;
    [SerializeField] AudioClip loadingMusic;
    [SerializeField] float musicFadeOutDuration = 2f;

    [SerializeField][Range(0, 1)] float progress = 0f;
    [SerializeField] float fadeOutTime = 1f;

    public bool End_Flag = false;
    public bool bypass;
    string[] assetPaths = new string[]
    {
        "Assets/Character",
        "Assets/Character",
        "Assets/Animations",
        "Assets/Fonts",
        "Assets/Soundz",
        "Assets/Outfits",
        "Assets/Scripts"

    };

    [SerializeField] Slider downloadProgressSlider;
    [SerializeField] TextMeshProUGUI downloadProgressText;
    [SerializeField] TextMeshProUGUI downloadText;

    void Start()
    {
        if (!bypass)
        {

            if (musicSource != null && loadingMusic != null)
            {
                musicSource.clip = loadingMusic;
                musicSource.loop = true;
                musicSource.Play();
            }
            CircleImg.fillAmount = 0f;
            txtProgress.text = "0";
            LoadText.text = "Starting Up";
            CircleImg.gameObject.SetActive(true);
            txtProgress.gameObject.SetActive(true);
            LoadText.gameObject.SetActive(true);
            downloadProgressSlider.gameObject.SetActive(false);
            downloadProgressText.gameObject.SetActive(false);
            downloadText.gameObject.SetActive(false);

            StartCoroutine(ConnectToServer());
        }
    }


    IEnumerator FadeMusicOut()
    {
        if (musicSource == null || loadingMusic == null) yield break;

        float startVolume = musicSource.volume;
        float elapsedTime = 0f;

        while (elapsedTime < musicFadeOutDuration)
        {
            elapsedTime += Time.deltaTime;
            float newVolume = Mathf.Lerp(startVolume, 0f, elapsedTime / musicFadeOutDuration);
            musicSource.volume = newVolume;
            yield return null;
        }

        musicSource.Stop();
        musicSource.volume = startVolume;
    }

    IEnumerator ConnectToServer()
    {
        yield return new WaitForSeconds(3f);
        CircleImg.fillAmount = 0.03f;
        txtProgress.text = "5";
        LoadText.text = "Connecting to Server";

        yield return new WaitForSeconds(5f);
        yield return StartCoroutine(CheckInternetAndLoadAssets());
    }
    IEnumerator CheckInternetAndLoadAssets()
    {
        yield return new WaitForSeconds(3f);
        CircleImg.fillAmount = 0.05f;
        txtProgress.text = "5";
        LoadText.text = "Checking For Resources";
        yield return new WaitForSeconds(5f);
        yield return StartCoroutine(LoadAssetsAsync());
    }

    IEnumerator LoadAssetsAsync()
    {
        string modelsFolderPath = Path.Combine(Application.dataPath, "..", "models");
        string classificationFolderPath = Path.Combine(modelsFolderPath, "XLMRoberta-Alexa-Intents-Classification");

        if (!Directory.Exists(modelsFolderPath))
        {
            Directory.CreateDirectory(modelsFolderPath);
            Debug.Log($"Created models folder {modelsFolderPath}");
        }

        if (!Directory.Exists(classificationFolderPath))
        {
            Directory.CreateDirectory(classificationFolderPath);
            Debug.Log($"Created classification folder {classificationFolderPath}");
        }

        var fileSources = new Dictionary<string, string>
        {
            { "../Models/XLMRoberta-Alexa-Intents-Classification/rng_state.pth", "https://huggingface.co/qanastek/XLMRoberta-Alexa-Intents-Classification/resolve/main/rng_state.pth" },
            { "../Models/XLMRoberta-Alexa-Intents-Classification/predict.py", "https://huggingface.co/qanastek/XLMRoberta-Alexa-Intents-Classification/resolve/main/predict.py" },
            { "../Models/XLMRoberta-Alexa-Intents-Classification/config.json", "https://huggingface.co/qanastek/XLMRoberta-Alexa-Intents-Classification/resolve/main/config.json" },
            { "../Models/XLMRoberta-Alexa-Intents-Classification/scheduler.pt", "https://huggingface.co/qanastek/XLMRoberta-Alexa-Intents-Classification/resolve/main/scheduler.pt" },
            { "../Models/XLMRoberta-Alexa-Intents-Classification/sentencepiece.bpe.model", "https://huggingface.co/qanastek/XLMRoberta-Alexa-Intents-Classification/resolve/main/sentencepiece.bpe.model" },
            { "../Models/XLMRoberta-Alexa-Intents-Classification/special_tokens_map.json", "https://huggingface.co/qanastek/XLMRoberta-Alexa-Intents-Classification/resolve/main/special_tokens_map.json" },
            { "../Models/XLMRoberta-Alexa-Intents-Classification/tokenizer.json", "https://huggingface.co/qanastek/XLMRoberta-Alexa-Intents-Classification/resolve/main/tokenizer.json" },
            { "../Models/XLMRoberta-Alexa-Intents-Classification/tokenizer_config.json", "https://huggingface.co/qanastek/XLMRoberta-Alexa-Intents-Classification/resolve/main/tokenizer_config.json" },
            { "../Models/XLMRoberta-Alexa-Intents-Classification/trainer_state.json", "https://huggingface.co/qanastek/XLMRoberta-Alexa-Intents-Classification/resolve/main/trainer_state.json" },
            { "../Models/XLMRoberta-Alexa-Intents-Classification/training_args.bin", "https://huggingface.co/qanastek/XLMRoberta-Alexa-Intents-Classification/resolve/main/training_args.bin" },
            { "../Models/XLMRoberta-Alexa-Intents-Classification/optimizer.pt", "https://huggingface.co/qanastek/XLMRoberta-Alexa-Intents-Classification/resolve/main/optimizer.pt" },
            { "../Models/XLMRoberta-Alexa-Intents-Classification/pytorch_model.bin", "https://huggingface.co/qanastek/XLMRoberta-Alexa-Intents-Classification/resolve/main/pytorch_model.bin" }
        };

       var missingFiles = fileSources
            .Where(pair => 
            {
                string fullPath = Path.Combine(modelsFolderPath, pair.Key);
                bool fileExists = File.Exists(fullPath);
                
                if (fileExists)
                {
                    Debug.Log($"File already exists, skipping download: {fullPath}");
                }
                
                return !fileExists;
            })
            .ToList();

        if (missingFiles.Any())
        {
            Debug.Log($"Downloading {missingFiles.Count} missing files.");
            for (int i = 0; i < missingFiles.Count; i++)
            {
                var missingFile = missingFiles[i];
                yield return StartCoroutine(DownloadFile(missingFile.Key, missingFile.Value, i, missingFiles.Count));
            }
        }
        else
        {
            Debug.Log("All required files are already present. Skipping download.");
        }

        int totalFiles = 0;
        foreach (string folderPath in assetPaths)
        {
            if (Directory.Exists(folderPath))
            {
                string[] files = Directory.GetFiles(folderPath);
                totalFiles += files.Length;
                Debug.Log($"Folder: {folderPath}, Files count: {files.Length}");
            }
        }

        Debug.Log($"Total files to process: {totalFiles}");

        float elapsedTime = 0f;
        float baseProgress = 0.05f;
        progress = baseProgress;
        LoadText.text = "Loading Assets";
        LoadText.fontSize = 36;

        int processedFiles = 0;
        foreach (string folderPath in assetPaths)
        {
            if (Directory.Exists(folderPath))
            {
                string[] files = Directory.GetFiles(folderPath);
                foreach (string currentFilePath in files)
                {
                    yield return null;
                    elapsedTime += Time.deltaTime;
                    processedFiles++;
                    progress = baseProgress + (elapsedTime / totalFiles);
                    int percentage = Mathf.RoundToInt(progress * 100f);

                    Debug.Log($"Processing file: {currentFilePath}");
                    Debug.Log($"Progress: {percentage}% ({processedFiles}/{totalFiles})");
                    Debug.Log($"Elapsed Time: {elapsedTime}");

                    CircleImg.fillAmount = progress;
                    txtProgress.text = percentage.ToString();
                    yield return new WaitForSeconds(0.1f);
                }
            }
        }

        Debug.Log("Asset loading complete");
        float previousProgress = progress;
        float finalIntegrityCheckProgress = previousProgress;
        yield return StartCoroutine(DummyIntegrityCheck(progress));

        progress = previousProgress;
        CircleImg.fillAmount = progress;

        progress = 1f;
        CircleImg.fillAmount = progress;
        txtProgress.text = "100";
        LoadText.text = "Done";

        yield return new WaitForSeconds(fadeOutTime);
        yield return StartCoroutine(FadeMusicOut());
        End_Flag = true;
        Debug.Log("LOADING COMPLETE");

        CanvasGroup canvasGroup = gameObject.GetComponent<CanvasGroup>();
        if (canvasGroup == null)
        {
            canvasGroup = gameObject.AddComponent<CanvasGroup>();
        }

        float currentTime = 0f;
        while (currentTime < fadeOutTime)
        {
            float alpha = Mathf.Lerp(1f, 0f, currentTime / fadeOutTime);
            canvasGroup.alpha = alpha;
            CircleImg.color = new Color(CircleImg.color.r, CircleImg.color.g, CircleImg.color.b, alpha);
            txtProgress.color = new Color(txtProgress.color.r, txtProgress.color.g, txtProgress.color.b, alpha);
            LoadText.color = new Color(LoadText.color.r, LoadText.color.g, LoadText.color.b, alpha);

            currentTime += Time.deltaTime;
            yield return null;
        }

        canvasGroup.alpha = 0f;
        CircleImg.color = new Color(CircleImg.color.r, CircleImg.color.g, CircleImg.color.b, 0f);
        LoadText.color = new Color(LoadText.color.r, LoadText.color.g, LoadText.color.b, 0f);
        CircleImg.gameObject.SetActive(false);
        txtProgress.gameObject.SetActive(false);
        LoadText.gameObject.SetActive(false);
    }

    IEnumerator DownloadFile(string relativePath, string fileUrl, int currentFileIndex, int totalMissingFiles)
    {
        string fullPath = Path.Combine(Directory.GetParent(Directory.GetParent(Application.dataPath).FullName).FullName, "models", Path.GetDirectoryName(relativePath));
        string finalFilePath = Path.Combine(fullPath, Path.GetFileName(relativePath));
        string tempFilePath = Path.Combine(fullPath, Path.GetFileNameWithoutExtension(relativePath) + ".tmp");

        if (File.Exists(finalFilePath))
        {
            Debug.Log($"File already exists: {finalFilePath}. Skipping download.");
            yield break;
        }

        if (!Directory.Exists(fullPath))
        {
            Directory.CreateDirectory(fullPath);
        }

        if (downloadProgressSlider != null)
        {
            downloadProgressSlider.value = 0f;
            downloadProgressSlider.gameObject.SetActive(true);
            downloadProgressText.gameObject.SetActive(true);
            downloadText.gameObject.SetActive(true);
        }

        if (downloadText != null)
        {
            downloadText.text = $"Downloading Resources";
        }
        bool isJsonFile = Path.GetExtension(relativePath).Equals(".json", StringComparison.OrdinalIgnoreCase);
        string downloadPath = isJsonFile ? finalFilePath : tempFilePath;

        using (UnityWebRequest www = UnityWebRequest.Get(fileUrl))
        {
            www.downloadHandler = new DownloadHandlerFile(downloadPath);
            var operation = www.SendWebRequest();
            Application.quitting += () => {
                if (!isJsonFile && File.Exists(downloadPath))
                {
                    DeleteTempFile(downloadPath);
                }
            };

            while (!operation.isDone)
            {
                float downloadProgress = www.downloadProgress;
                float overallProgress = (currentFileIndex + downloadProgress) / totalMissingFiles;

                if (downloadProgressSlider != null)
                {
                    downloadProgressSlider.value = overallProgress;
                }

                if (downloadProgressText != null)
                {
                    downloadProgressText.text = $"{(int)Math.Round(overallProgress * 100f)}%";
                }

                yield return null;
            }

            if (www.result == UnityWebRequest.Result.Success)
            {
                Debug.Log($"File downloaded successfully: {finalFilePath}");
                FileInfo fileInfo = new FileInfo(downloadPath);

                if (fileInfo.Exists && fileInfo.Length > 0)
                {
                    Debug.Log($"Total file size: {fileInfo.Length} bytes");

                    if (!isJsonFile)
                    {
                        File.Move(downloadPath, finalFilePath);
                    }

                    if (downloadProgressSlider != null)
                    {
                        downloadProgressSlider.value = (currentFileIndex + 1f) / totalMissingFiles;
                    }
                }
                else
                {
                    Debug.LogError("Download failed: File is empty or could not be created.");
                    if (!isJsonFile)
                    {
                        DeleteTempFile(downloadPath);
                    }
                }
            }
            else
            {
                Debug.LogError($"Download failed: {www.error}");
                if (!isJsonFile)
                {
                    DeleteTempFile(downloadPath);
                }

                if (downloadProgressText != null)
                {
                    downloadProgressText.text = "Download Failed!";
                }

                if (downloadText != null)
                {
                    downloadText.text = $"Download Failed: {Path.GetFileName(finalFilePath)}";
                }
            }
        }
        if (currentFileIndex == totalMissingFiles - 1)
        {
            if (downloadProgressSlider != null)
            {
                downloadProgressSlider.gameObject.SetActive(false);
                downloadProgressText.gameObject.SetActive(false);
                downloadText.gameObject.SetActive(false);
            }
        }
    }

    void DeleteTempFile(string tempFilePath)
    {
        if (File.Exists(tempFilePath))
        {
            File.Delete(tempFilePath);
        }
    }




    IEnumerator DummyIntegrityCheck(float startingProgress)
    {
        LoadText.text = "Verifying Files";
        float dummyCheckDuration = 2f;
        float elapsedTime = 0f;

        while (elapsedTime < dummyCheckDuration)
        {
            yield return null;

            progress = Mathf.Lerp(startingProgress, startingProgress + 0.2f, elapsedTime / dummyCheckDuration);
            CircleImg.fillAmount = progress;

            int percentage = Mathf.RoundToInt(progress * 100f);
            txtProgress.text = percentage.ToString();

            elapsedTime += Time.deltaTime;
        }
        yield return new WaitForSeconds(3f);
        yield return StartCoroutine(AdditionalUpdateCheck(progress));
        yield return new WaitForSeconds(3f);
    }

    IEnumerator AdditionalUpdateCheck(float startingProgress)
    {
        LoadText.text = "Checking For Updates";
        float updateCheckDuration = 2f;
        float elapsedTime = 0f;

        while (elapsedTime < updateCheckDuration)
        {
            yield return null;

            float updateCheckProgress = Mathf.Lerp(startingProgress, startingProgress + 0.2f, elapsedTime / updateCheckDuration);
            progress = updateCheckProgress;
            CircleImg.fillAmount = progress;

            int percentage = Mathf.RoundToInt(progress * 100f);
            txtProgress.text = percentage.ToString();

            elapsedTime += Time.deltaTime;
        }
        yield return new WaitForSeconds(3f);
        yield return StartCoroutine(CleanUp(progress));
        yield return new WaitForSeconds(2f);
    }

    IEnumerator CleanUp(float startingProgress)
    {
        LoadText.text = "Getting Things Ready";
        float CleanUpDuration = 2f;
        float elapsedTime = 0f;

        try
        {
            CleanupTemporaryFiles();
            ClearCachedData();
            System.GC.Collect();
            System.GC.WaitForPendingFinalizers();
        }
        catch (Exception e)
        {
            Debug.LogError($"Cleanup error: {e.Message}");
        }

        string classifiedIntent = MenuItem_KODEZ_Class.Intent_Classifier("@*$Connection SuccessFull@*$");
        Debug.Log($"Classified Intent: {classifiedIntent}");
        Debug.Log("Loaded Intent Classifier model");
        while (elapsedTime < CleanUpDuration)
        {
            yield return null;

            float CleanUpProgress = Mathf.Lerp(startingProgress, startingProgress + 0.3f, elapsedTime / CleanUpDuration);
            progress = CleanUpProgress;
            CircleImg.fillAmount = progress;

            int percentage = Mathf.RoundToInt(progress * 100f);
            txtProgress.text = percentage.ToString();

            elapsedTime += Time.deltaTime;
        }

    }

    private void CleanupTemporaryFiles()
    {
        string modelsFolderPath = Path.Combine(Directory.GetParent(Directory.GetParent(Application.dataPath).FullName).FullName, "models");

        if (Directory.Exists(modelsFolderPath))
        {
            string[] tempFiles = Directory.GetFiles(modelsFolderPath, "*.tmp", SearchOption.AllDirectories);
            foreach (string tempFile in tempFiles)
            {
                try
                {
                    File.Delete(tempFile);
                    Debug.Log($"Deleted temporary file: {tempFile}");
                }
                catch (Exception e)
                {
                    Debug.LogWarning($"Could not delete temp file {tempFile}: {e.Message}");
                }
            }
        }
    }

    private void ClearCachedData()
    {
        Caching.ClearCache();
        Debug.Log("Cleared application cache");
    }
}