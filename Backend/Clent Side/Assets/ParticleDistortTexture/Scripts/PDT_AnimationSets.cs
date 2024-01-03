using UnityEngine;
using System.Collections;

public class PDT_AnimationSets : MonoBehaviour 
{
	public string KeyboardKEY = "";
	
	public Animator[] animatorList;
	public string[] stateName;

	private RaycastHit hit;
	private Ray ray;
	
	public ParticleSystem[] particleList;

	void Start () 
	{

	
	}
	
	void Update () 
	{
		if(Input.GetKeyDown(KeyboardKEY) && KeyboardKEY != "")
			PlayAll();

		if (Input.GetMouseButton(0))
		{
			
			hit = new RaycastHit();
			ray = Camera.main.ScreenPointToRay (Input.mousePosition);
			if(Physics.Raycast(ray, out hit))
			{
				if(hit.collider.transform.gameObject == this.gameObject)
				{
					PlayAll();
				}
			}
		}
	}

	public void PlayAll()
	{
		//===
		for (int i=0; i<animatorList.Length; i++)
		{
			animatorList[i].Play(stateName[i], -1, 0f);

		}
		//===
		for (int i=0; i<particleList.Length; i++)
		{
			particleList[i].Play();
		}
		//===
		
	}

}
