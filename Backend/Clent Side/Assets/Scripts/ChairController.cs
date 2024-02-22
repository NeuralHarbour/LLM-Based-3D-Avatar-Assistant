using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class ChairController : MonoBehaviour
{
    public GameObject Chair;
    public Animator chair_animator;
    // Start is called before the first frame update
    void Start()
    {
        if (Chair == null)
        {
            Debug.LogError("No game object assigned to this script!");
            return;
        }

        if (!Chair.activeSelf)
        {
            Debug.Log("Chair Hidden");
        }
        else
        {
            Debug.Log("Chair Active");
        }
        if (chair_animator == null)
        {
            Debug.LogError("No Animator component found on the game object!");
        }
    }

    // Update is called once per frame
    void Update()
    {
        
    }
    public void HideChair()
    {
        if (Chair != null)
        {
            Chair.SetActive(false);
        }
        else
        {
            Debug.LogWarning("No game object assigned to hide!");
        }
    }

    public void ShowChair()
    {
        if (Chair != null)
        {
            Chair.SetActive(true);
        }
        else
        {
            Debug.LogWarning("No game object assigned to hide!");
        }
    }

    public void PlayFloatAnim()
    {
        chair_animator.SetTrigger("StartFloat");
    }
    public void PlayDisappearAnim()
    {
        chair_animator.SetTrigger("Disappear");
    }
}
