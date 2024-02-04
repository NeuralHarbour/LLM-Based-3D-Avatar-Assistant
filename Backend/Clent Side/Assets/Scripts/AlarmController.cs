using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class AlarmController : MonoBehaviour
{
    public GameObject gameobject;
    public Animator alarm_animator;
    // Start is called before the first frame update
    void Start()
    {
        if (gameobject == null)
        {
            Debug.LogError("No game object assigned to this script!");
            return;
        }

        if (!gameobject.activeSelf)
        {
            Debug.Log("Alarm Hidden");
        }
        else
        {
            Debug.Log("Alarm Active");
        }
        if (alarm_animator == null)
        {
            Debug.LogError("No Animator component found on the game object!");
        }
    }

    // Update is called once per frame
    void Update()
    {

    }

    public void HideGameObject()
    {
        if (gameobject != null)
        {
            gameobject.SetActive(false);
        }
        else
        {
            Debug.LogWarning("No game object assigned to hide!");
        }
    }

    public void ShowAlarm()
    {
        if (gameobject != null)
        {
            gameobject.SetActive(true);
        }
        else
        {
            Debug.LogWarning("No game object assigned to hide!");
        }
    }

    public void PlayFloatAnim()
    {
        alarm_animator.SetTrigger("Start_Float");
    }
    public void PlayDisappearAnim()
    {
        alarm_animator.SetTrigger("FadeOutAlarm");
    }
}
