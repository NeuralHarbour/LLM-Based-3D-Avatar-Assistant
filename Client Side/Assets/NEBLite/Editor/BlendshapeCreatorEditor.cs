//////////////////////////////////////////////////////
///        © Copyright 2023 - ReForge Mode         ///
/// See the LICENSE file for licensing information ///
//////////////////////////////////////////////////////

using System.Collections;
using System.Collections.Generic;
using UnityEngine;

#if UNITY_EDITOR
using UnityEditor;

namespace NotEnoughBlendshape
{
    [CustomEditor(typeof(BlendshapeCreator))]
    public class BlendshapeCreatorEditor : Editor
    {
        private BlendshapeCreator creator;

        private bool isFieldMeshNotNull = false;
        private bool isSourceMeshExist = false;
        private bool isTargetMeshExist = false;
        private bool isMeshDifferent = false;
        private bool isMeshVertexCountMatch = false;
        private bool isFieldNameNotNull = false;
        private bool isBlendshapeNameNotExist = false;

        //Color for the Custom Editor warning
        public Color colorWarning = Color.yellow;

        public void OnEnable()
        {
            creator = (BlendshapeCreator)target;
        }

        public override void OnInspectorGUI()
        {
            //DrawDefaultInspector();

            FieldValidation();

            DisplayGuideMessage();

            DisplaySourceField();
            DisplayTargetField();
            DisplayNameField();

            bool validCheck = isFieldMeshNotNull && isSourceMeshExist && isTargetMeshExist && 
                              isMeshVertexCountMatch && isMeshDifferent && 
                              isFieldNameNotNull && isBlendshapeNameNotExist;
            EditorGUI.BeginDisabledGroup(!validCheck);
            {
                DisplayButton();
            }
            EditorGUI.EndDisabledGroup();
        }

        public void DisplaySourceField()
        {
            if (!isSourceMeshExist || !isMeshDifferent || !isMeshVertexCountMatch)
                GUI.color = colorWarning;

            EditorGUILayout.BeginHorizontal();
            EditorGUILayout.LabelField("Source Mesh", GUILayout.Width(150f));
            creator.sourceMeshRenderer = (SkinnedMeshRenderer)EditorGUILayout.ObjectField(creator.sourceMeshRenderer, typeof(SkinnedMeshRenderer), true, GUILayout.ExpandWidth(true));
            EditorGUILayout.EndHorizontal();

            GUI.color = Color.white;
        }

        public void DisplayTargetField()
        {
            if (!isTargetMeshExist || !isMeshDifferent || !isMeshVertexCountMatch)
                GUI.color = colorWarning;

            EditorGUILayout.BeginHorizontal();
            EditorGUILayout.LabelField("Target Mesh", GUILayout.Width(150f));
            creator.targetMeshRenderer = (SkinnedMeshRenderer)EditorGUILayout.ObjectField(creator.targetMeshRenderer, typeof(SkinnedMeshRenderer), true, GUILayout.ExpandWidth(true));
            EditorGUILayout.EndHorizontal();

            GUI.color = Color.white;
        }

        public void FieldValidation()
        {
            //Set everything back to default true. Mostly for color notification.
            isFieldMeshNotNull = true;
            isSourceMeshExist = true;
            isTargetMeshExist = true;
            isMeshDifferent = true;
            isMeshVertexCountMatch = true;
            isFieldNameNotNull = true;
            isBlendshapeNameNotExist = true;


            //Check if the any of the Source and Target field is empty
            isFieldMeshNotNull = (creator.sourceMeshRenderer != null && creator.targetMeshRenderer != null);
            if (isFieldMeshNotNull == false) return;

            //Check if the mesh is assigned at the Source SkinnedMeshRenderer
            isSourceMeshExist = creator.sourceMeshRenderer.sharedMesh != null;
            if (isSourceMeshExist == false) return;

            //Check if the mesh is assigned at the Target SkinnedMeshRenderer
            isTargetMeshExist = creator.targetMeshRenderer.sharedMesh != null;
            if (isTargetMeshExist == false) return;

            //Check if the Source and Target are two different models
            isMeshDifferent = CheckIsMeshDifferent(creator.sourceMeshRenderer, creator.targetMeshRenderer);
            if (isMeshDifferent == false) return;

            //Check for the vertex count mismatch between Source and Target mesh
            int sourceVertexCount = creator.sourceMeshRenderer.sharedMesh.vertexCount;
            int targetVertexCount = creator.targetMeshRenderer.sharedMesh.vertexCount;
            isMeshVertexCountMatch = (sourceVertexCount == targetVertexCount);
            if (isMeshVertexCountMatch == false) return;

            //Check if the new blendshape has already assigned a name in the field
            isFieldNameNotNull = (creator.newBlendshapeName.Length > 0);
            if (isFieldNameNotNull == false) return;

            //Check if the blendshape name already exists in the Target model
            isBlendshapeNameNotExist = !CheckBlendshapeExist(creator.newBlendshapeName);
            if (isBlendshapeNameNotExist == false) return;
        }

        public void DisplayNameField()
        {
            if (!isFieldNameNotNull || !isBlendshapeNameNotExist)
                GUI.color = colorWarning;

            EditorGUILayout.BeginHorizontal();
            EditorGUILayout.LabelField("New Blendshape Name", GUILayout.Width(150f));
            creator.newBlendshapeName = EditorGUILayout.TextField(creator.newBlendshapeName, GUILayout.ExpandWidth(true));
            EditorGUILayout.EndHorizontal();

            GUI.color = Color.white;
        }

        public void DisplayButton()
        {
            if (GUILayout.Button("Create Blendshape", GUILayout.Height(50)))
            {
                creator.CreateBlendshape();
            }
        }

        /// <summary>
        /// Lists all possible combinations of Source, Target, and Name fields conditions
        /// </summary>
        public void DisplayGuideMessage()
        {
            if (isFieldMeshNotNull == false)
            {
                EditorGUILayout.HelpBox("This is a tool to create a new blendshape from the differences between two models \n" +
                                        "Drag in your Source and Target SkinnedMeshRenderer components into these two fields. \n" +
                                        "Note that only the Target got the final blendshape.", MessageType.Info);
                return;
            }

            if (isSourceMeshExist == false)
            {
                EditorGUILayout.HelpBox("Error! Source SkinnedMeshRenderer doesn't have a mesh assigned to it! \n" +
                                        "Please replace the Source field with other SkinnedMeshRenderer component.", MessageType.Warning);
                return;
            }

            if (isTargetMeshExist == false)
            {
                EditorGUILayout.HelpBox("Error! Target SkinnedMeshRenderer doesn't have a mesh assigned to it! \n" +
                                        "Please replace the Target field with other SkinnedMeshRenderer component.", MessageType.Warning);
                return;
            }

            if (isMeshDifferent == false)
            {
                EditorGUILayout.HelpBox("Error! Source Mesh and Target Mesh are the exact same model! \n" +
                                        "Please assign a different SkinnedMeshRenderer to replace either of them.\"", MessageType.Warning);
                return;
            }

            if (isMeshVertexCountMatch == false)
            {
                EditorGUILayout.HelpBox("Error! Vertex count mismatch between Source and Target models! \n" +
                                        "Make sure to only put two of the same VRM model with slight different physical settings in VRoid Studio", MessageType.Warning);
                return;
            }

            if(isFieldNameNotNull == false)
            {
                EditorGUILayout.HelpBox("Make sure to type in a name for your new blendshapes in the \"New Blendshape Name\" field", MessageType.Warning);
                return;
            }

            if(isBlendshapeNameNotExist == false)
            {
                EditorGUILayout.HelpBox("Error! Blendshape name already exists! Change the name to another name!", MessageType.Warning);
                return;
            }

            EditorGUILayout.HelpBox("Alright! Click on the button to create a new blendshape!", MessageType.Info);
        }

        /// <summary>
        /// Compare two gameobjects. This also compares if the same object is the 
        /// instanced model or asset model in the Project Window.
        /// </summary>
        /// <param name="model1"></param>
        /// <param name="model2"></param>
        /// <returns>True if the model is the same. Returns false otherwise.</returns>
        private bool CheckIsMeshDifferent(SkinnedMeshRenderer mesh1, SkinnedMeshRenderer mesh2)
        {
            if (mesh1 == null || mesh2 == null)
            {
                return true;
            }

            if (mesh1 == mesh2)
            {
                return false;
            }

            string prefabAssetPath1 = PrefabUtility.GetPrefabAssetPathOfNearestInstanceRoot(mesh1);
            string prefabAssetPath2 = PrefabUtility.GetPrefabAssetPathOfNearestInstanceRoot(mesh2);

            if (prefabAssetPath1 == null || prefabAssetPath2 == null)
            {
                return true;
            }

            if (prefabAssetPath1 == prefabAssetPath2)
            {
                return false;
            }

            return true;
        }

        private bool CheckBlendshapeExist(string blendshapeName)
        {
            if(creator.targetMeshRenderer.sharedMesh.blendShapeCount <= 0)
            {
                return false;
            }

            for (int i = 0; i < creator.targetMeshRenderer.sharedMesh.blendShapeCount; i++)
            {
                if (creator.targetMeshRenderer.sharedMesh.GetBlendShapeName(i) == blendshapeName)
                {
                    return true;
                }
            }
            return false;
        }
    }
}
#endif