using UnityEngine;
using System.Collections;
using UnityEngine.SceneManagement;

public class PDT_ChangeScene : MonoBehaviour 
{
	public string KeyboardKEY = "";
	//public Object thescene;
	public string SceneName="";

	private RaycastHit hit;
	private Ray ray;

	void Start () 
	{
		//SceneName = thescene.name;
	
	}
	
	void Update () 
	{

		if (Input.GetMouseButton(0))
		{
			
			hit = new RaycastHit();
			ray = Camera.main.ScreenPointToRay (Input.mousePosition);
			if(Physics.Raycast(ray, out hit))
			{
				if(hit.collider.transform.gameObject == this.gameObject)
				{
					SceneManager.LoadScene(SceneName);
				}
			}
		}



		if(Input.GetKeyDown(KeyboardKEY) && KeyboardKEY != "")
			SceneManager.LoadScene(SceneName);
	}


}
