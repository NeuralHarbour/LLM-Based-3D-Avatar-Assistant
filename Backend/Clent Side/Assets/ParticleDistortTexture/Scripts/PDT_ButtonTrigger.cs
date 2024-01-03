using UnityEngine;
using System.Collections;

public class PDT_ButtonTrigger : MonoBehaviour 
{
	public int butno=1;
	public PDT_GameController gc;
	private RaycastHit hit;
	private Ray ray;

	// Use this for initialization
	void Start () 
	{

	}
	
	// Update is called once per frame
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
					switch(butno)
					{
					case 1: gc.b_top=true;break;
					case 2: gc.b_bot=true;break;
					case 3: gc.b_left=true;break;
					case 4: gc.b_right=true;break;
					default: break;
					}
				}
			}
		}
		else
		{
			gc.b_top=false;
			gc.b_bot=false;
			gc.b_left=false;
			gc.b_right=false;
		}
	}



}
