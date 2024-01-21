using UnityEngine;
using UnityEngine.UI;
using TMPro;
using System.Collections;
using System.IO;

public class Integrity_Loader : MonoBehaviour
{
    [SerializeField] Image CircleImg;
    [SerializeField] TextMeshProUGUI txtProgress;
    [SerializeField] Text LoadText;

    [SerializeField][Range(0, 1)] float progress = 0f;
    [SerializeField] float fadeOutTime = 1f;

    WsClient ws;

    [SerializeField] Font japaneseFont;
    [SerializeField] Font russianFont;
    [SerializeField] Font defaultFont;

    public bool End_Flag = false;
    string[] assetPaths = new string[]
    {
        "Assets/Character",
        "Assets/PNG's",
        "Assets/Scripts",
        "Assets/VoicevoxBridge",
        "Assets/Fonts",
        "Assets/Messages",
        "Assets/Scifi Things",
        "Assets/Sounds",
        // Add more paths as needed for different types of assets
    };

    void Start()
    {
        ws = GameObject.FindGameObjectWithTag("Middleware").GetComponent<WsClient>();
        CircleImg.fillAmount = 0f;
        txtProgress.text = "0";
        CircleImg.gameObject.SetActive(true);
        txtProgress.gameObject.SetActive(true);
        LoadText.gameObject.SetActive(true);

        StartCoroutine(CheckInternetAndLoadAssets());
    }

    IEnumerator CheckInternetAndLoadAssets()
    {
        yield return new WaitForSeconds(3f);

        if (Application.internetReachability != NetworkReachability.NotReachable)
        {
            Debug.Log("Country : " + ws.country);
            if(ws.country == "JP")
            {
                LoadText.font = japaneseFont;
                LoadText.fontStyle = FontStyle.Normal;
            }
            else if(ws.country == "RU")
            {
                LoadText.font = russianFont;
            }
            else
            {
                LoadText.font = defaultFont;
            }
            Debug.Log("Internet connection available. Loading assets...");
            // Set initial progress to 5%
            CircleImg.fillAmount = 0.05f;
            txtProgress.text = "5";
            yield return StartCoroutine(LoadAssetsAsync());
        }
        else
        {
            Debug.LogError("No internet connection. Handle accordingly.");
            // Set initial progress to 5%
            CircleImg.fillAmount = 0.05f;
            txtProgress.text = "5";
            yield return StartCoroutine(LoadAssetsAsync());
        }
    }

    IEnumerator LoadAssetsAsync()
    {
        int totalFiles = 0;
        foreach (string folderPath in assetPaths)
        {
            string[] files = Directory.GetFiles(folderPath);
            totalFiles += files.Length;
        }

        float elapsedTime = 0f;

        // Start from 5% progress
        float baseProgress = 0.05f;
        progress = baseProgress;
        if (ws.country == "JP")
        {
            LoadText.text = "アセットのロード";
            LoadText.fontSize = 50;
        }
        else if(ws.country == "RU")
        {
            LoadText.text = "Загрузка ресурсов";
            LoadText.fontSize = 60;
        }
        else
        {
            LoadText.text = "Loading Assets";
            LoadText.fontSize = 36;
        }
        foreach (string folderPath in assetPaths)
        {
            string[] files = Directory.GetFiles(folderPath);

            foreach (string filePath in files)
            {
                yield return null;

                elapsedTime += Time.deltaTime;
                progress = baseProgress + (elapsedTime / totalFiles);

                CircleImg.fillAmount = progress;

                int percentage = Mathf.RoundToInt(progress * 100f);
                txtProgress.text = percentage.ToString();

                yield return new WaitForSeconds(0.1f);
            }
        }
        float previousProgress = progress;
        float finalIntegrityCheckProgress = previousProgress;

        // Perform dummy integrity check
        yield return StartCoroutine(DummyIntegrityCheck(previousProgress));


        progress = previousProgress;
        CircleImg.fillAmount = progress;

        progress = 1f;
        CircleImg.fillAmount = progress;
        txtProgress.text = "100";
        if (ws.country == "JP")
        {
            LoadText.text = "終わり";
            LoadText.fontSize = 50;
        }
        else if(ws.country == "RU")
        {
            LoadText.text = "готово";
        }
        else
        {
            LoadText.text = "Done";
        }

        yield return new WaitForSeconds(fadeOutTime);
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
            yield return null; // Wait for the next frame
        }

        canvasGroup.alpha = 0f;
        CircleImg.color = new Color(CircleImg.color.r, CircleImg.color.g, CircleImg.color.b, 0f);
        LoadText.color = new Color(LoadText.color.r, LoadText.color.g, LoadText.color.b, 0f);
        CircleImg.gameObject.SetActive(false);
        txtProgress.gameObject.SetActive(false);
        LoadText.gameObject.SetActive(false);

    }

    IEnumerator DummyIntegrityCheck(float startingProgress)
    {
        if (ws.country == "JP")
        {
            LoadText.text = "ファイルの検証";
            LoadText.fontSize = 50;
        }
        else if(ws.country == "RU")
        {
            LoadText.text = "Проверка файлов";
        }
        else
        {
            LoadText.text = "Verifying Files";
        }
        // Simulate a dummy integrity check
        float dummyCheckDuration = 2f;
        float elapsedTime = 0f;

        while (elapsedTime < dummyCheckDuration)
        {
            yield return null;

            // Calculate progress based on the time elapsed and the starting progress
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
        if (ws.country == "JP")
        {
            LoadText.text = "アップデートの確認";
            LoadText.fontSize = 50;
        }
        else if(ws.country == "RU")
        {
            LoadText.text = "Проверка обновлений";
        }
        else
        {
            LoadText.text = "Checking For Updates";
        }
        // Simulate an additional update check
        float updateCheckDuration = 2f;
        float elapsedTime = 0f;

        while (elapsedTime < updateCheckDuration)
        {
            yield return null;

            // Continue from the progress of the integrity check
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
        if (ws.country == "JP")
        {
            LoadText.text = "準備を整える";
            LoadText.fontSize = 50;
        }
        else if(ws.country == "RU")
        {
            LoadText.text = "Подготовка к запуску";
        }
        else
        {
            LoadText.text = "Getting Things Ready";
        }
        float CleanUpDuration = 2f;
        float elapsedTime = 0f;

        while (elapsedTime < CleanUpDuration)
        {
            yield return null;

            // Continue from the progress of update check
            float CleanUpProgress = Mathf.Lerp(startingProgress, startingProgress + 0.3f, elapsedTime / CleanUpDuration);
            progress = CleanUpProgress;
            CircleImg.fillAmount = progress;

            int percentage = Mathf.RoundToInt(progress * 100f);
            txtProgress.text = percentage.ToString();

            elapsedTime += Time.deltaTime;
        }

    }
}
