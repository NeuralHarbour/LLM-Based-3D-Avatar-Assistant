using UnityEngine;
using System.Collections.Generic;

#if UNITY_EDITOR
using UnityEditor;
#endif

public class ShoeHeight : MonoBehaviour
{
    public Dictionary<Transform, List<GameObject>> playerShoePrefabs = new Dictionary<Transform, List<GameObject>>();

    void Start()
    {
        InitializePlayerShoePrefabs();
    }

    void InitializePlayerShoePrefabs()
    {
        Transform[] children = GetComponentsInChildren<Transform>(true);
        foreach (Transform child in children)
        {
            if (child.CompareTag("Player"))
            {
                Transform[] playerChildren = child.GetComponentsInChildren<Transform>(true);
                List<GameObject> playerShoes = new List<GameObject>();
                foreach (Transform playerChild in playerChildren)
                {
                    if (playerChild.CompareTag("Shoe"))
                    {
                        for (int i = 0; i < playerChild.childCount; i++)
                        {
                            Transform shoeChild = playerChild.GetChild(i);
                            playerShoes.Add(shoeChild.gameObject);
                        }
                    }
                }
                playerShoePrefabs.Add(child, playerShoes);
            }
        }
    }

    public void ToggleShoePrefabActiveState(GameObject shoePrefab)
    {
        foreach (var kvp in playerShoePrefabs)
        {
            foreach (var prefab in kvp.Value)
            {
                if (prefab != shoePrefab)
                {
                    prefab.SetActive(false);
                }
            }
        }
        shoePrefab.SetActive(!shoePrefab.activeSelf);
    }

    // Update is called once per frame
    void Update()
    {

    }
}

#if UNITY_EDITOR
[CustomEditor(typeof(ShoeHeight))]
public class PlayerShoePrefabsInspector : Editor
{
    public override void OnInspectorGUI()
    {
        base.OnInspectorGUI();

        ShoeHeight script = (ShoeHeight)target;

        EditorGUILayout.Space();

        EditorGUILayout.LabelField("Player Fields");

        foreach (var kvp in script.playerShoePrefabs)
        {
            bool isPlayerActive = kvp.Key.gameObject.activeSelf;
            string labelText = "Player: " + kvp.Key.name + " (Active: " + isPlayerActive.ToString() + ")";
            EditorGUILayout.LabelField(labelText);

            foreach (var shoePrefab in kvp.Value)
            {
                EditorGUILayout.BeginHorizontal();
                EditorGUILayout.ObjectField(shoePrefab, typeof(GameObject), true);
                bool isActive = shoePrefab.activeSelf;
                if (GUILayout.Button(isActive ? "Deactivate" : "Activate"))
                {
                    script.ToggleShoePrefabActiveState(shoePrefab);
                }
                EditorGUILayout.EndHorizontal();
            }
        }
    }
}
#endif
