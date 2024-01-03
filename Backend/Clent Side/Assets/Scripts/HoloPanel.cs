using System.Collections;
using UnityEngine;

public class HoloPanel : MonoBehaviour
{
    private Animator animator;

    void Start()
    {
        animator = GetComponent<Animator>();
        if (animator != null)
        {
            Debug.LogWarning("Holo Animator component found on " + gameObject.name);
        }
        else
        {
            Debug.LogWarning("Animator component not found on " + gameObject.name);
        }
    }

    public void OpenUp()
    {
        gameObject.SetActive(true);

        // Check if animator is null, attempt to get the component if it's null
        if (animator == null)
        {
            animator = GetComponent<Animator>();
            if (animator == null)
            {
                Debug.LogError("Animator component not found on " + gameObject.name + " in HoloPanel.OpenUp()");
                return;
            }
        }

        animator.SetTrigger("Appear");
        Invoke("CloseAfterDelay", 25f);
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
        // Wait until the "Disappear" animation finishes playing
        yield return new WaitForSeconds(animator.GetCurrentAnimatorStateInfo(0).length);

        // After the animation finishes, hide the GameObject
        Hidden();
    }

    public void Hidden()
    {
        gameObject.SetActive(false);
    }
    public void active()
    {
        gameObject.SetActive(true);
    }
}
