using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class WeatherText : MonoBehaviour
{
    private Animator animator;
    // Start is called before the first frame update
    void Start()
    {
        animator = GetComponent<Animator>();
    }

    // Update is called once per frame
    void Update()
    {
           
    }
    public void LoadText()
    {
        Active();

        // Check if animator is null, attempt to get the component if it's null
        if (animator == null)
        {
            animator = GetComponent<Animator>();
            if (animator == null)
            {
                return;
            }
        }

        animator.SetTrigger("Appear");
        Invoke("CloseAfterDelay", 20f);
    }
    private void CloseAfterDelay()
    {
        Close();
    }

    public void Close()
    {
        if (animator != null)
        {
            animator.SetTrigger("Disappear");
            StartCoroutine(WaitForAnimation());
        }
        else
        {
            Debug.LogError("Animator is null in HoloPanel.Close() method!");
        }
    }


    IEnumerator WaitForAnimation()
    {
        yield return new WaitForSeconds(animator.GetCurrentAnimatorStateInfo(0).length);
        Hide();
    }
    public void Hide()
    {
        gameObject.SetActive(false);
    }
    public void Active()
    {
        gameObject.SetActive(true);
    }

}
