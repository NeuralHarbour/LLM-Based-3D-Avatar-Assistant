using UnityEngine;
using System.Collections;

public class PDT_Drag : MonoBehaviour 
{

	public Transform mTrans;
	
	private float _sensitivity= 0.4f;
	private float _mouseReference;
	private float _mouseOffset;
	private Vector3 _rotation=Vector3.zero;
	private bool _isRotating;


	private RaycastHit hit;
	private Ray ray;
	
	// Use this for initialization
	void Start () 
	{
		//mTrans=this.transform;
	}
	
	// Update is called once per frame
	void Update () 
	{
		if (Input.GetMouseButtonDown(0))
		{
			
			hit = new RaycastHit();
			ray = Camera.main.ScreenPointToRay (Input.mousePosition);
			if(Physics.Raycast(ray, out hit))
			{
				if(hit.collider.transform.gameObject == this.gameObject)
				{
					_mouseReference = Input.mousePosition.x;
				}
			}
		}

		if (Input.GetMouseButton(0))
		{
			
			hit = new RaycastHit();
			ray = Camera.main.ScreenPointToRay (Input.mousePosition);
			if(Physics.Raycast(ray, out hit))
			{
				if(hit.collider.transform.gameObject == this.gameObject)
				{
					_mouseOffset = (Input.mousePosition.x - _mouseReference);
					_rotation.y = -(_mouseOffset + _mouseOffset) * _sensitivity;
					mTrans.Rotate(_rotation);
					_mouseReference = Input.mousePosition.x;
				}
			}
		}
	}
	
}
