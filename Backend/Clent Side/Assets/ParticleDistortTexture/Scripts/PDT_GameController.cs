using UnityEngine;
using System.Collections;

public class PDT_GameController : MonoBehaviour 
{
	
	private Transform player;

	public Transform player1;
	//private int currentfx=0; //start from 0, 33 is last
	//private int spacing=4;
	//public Transform player2;
	//public GameObject player1_current;
	//public GameObject player2_current;
	public Transform l_top;
	public Transform l_bot;
	public Transform l_left;
	public Transform l_right;
	public bool b_top = false;
	public bool b_bot = false;
	public bool b_left = false;
	public bool b_right = false;

	public float speed=1;
	//private bool isplayer1=true;
	//
	// Use this for initialization
	void Start () 
	{
		player = player1;
	}
	
	// Update is called once per frame
	void Update () 
	{
		//WALK VERTICAL
		if (Input.GetKey(KeyCode.W) || Input.GetKey(KeyCode.UpArrow) || b_top)
		{
			if(player.localPosition.x-speed >= l_top.localPosition.x)
				player.localPosition = new Vector3(player.localPosition.x-speed,player.localPosition.y,player.localPosition.z);
		}
		else
		{
			if (Input.GetKey(KeyCode.S) || Input.GetKey(KeyCode.DownArrow) || b_bot)
			{
				if(player.localPosition.x+speed <= l_bot.localPosition.x)
					player.localPosition = new Vector3(player.localPosition.x+speed,player.localPosition.y,player.localPosition.z);
			}
		}
		
		//WALK HORIAONTAL
		if (Input.GetKey(KeyCode.A) || Input.GetKey(KeyCode.LeftArrow) || b_left)
		{
			if(player.localPosition.z-speed >= l_left.localPosition.z)
				player.localPosition = new Vector3(player.localPosition.x,player.localPosition.y,player.localPosition.z-speed);
		}
		else
		{
			if (Input.GetKey(KeyCode.D) || Input.GetKey(KeyCode.RightArrow) || b_right)
			{
				if(player.localPosition.z+speed <= l_right.localPosition.z)
					player.localPosition = new Vector3(player.localPosition.x,player.localPosition.y,player.localPosition.z+speed);
			}
		}
	}
	

}
