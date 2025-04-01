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
    [CustomEditor(typeof(BlendshapeTransfer))]
    public class BlendshapeTransferEditor : Editor
    {
        private BlendshapeTransfer nebTool;

        //Field Validation variables
        private bool isFieldNotNull;
        private bool isSourceFaceExist;
        private bool isTargetFaceExist;
        private bool isSourceSkinnedMeshExist;
        private bool isTargetSkinnedMeshExist;
        private bool isSourceMeshExist;
        private bool isTargetMeshExist;
        private bool isModelDifferent;
        private bool isVertexCountMatched;

        //Optimization variables
        private Object lastKnownSource;
        private Object lastKnownTarget;

        //Color for the Custom Editor warning
        public Color colorWarning = Color.yellow;

        private void OnEnable()
        {
            nebTool = (BlendshapeTransfer)target;
        }

        public override void OnInspectorGUI()
        {
            FieldValidation();

            if (nebTool.isAdvancedMode == false) DisplayGuideMessage();
            else DisplayGuideMessage_AdvancedMode();

            DisplaySourceField();
            DisplayTargetField();
            DisplayButton();

            DisplayAdvancedToggle();

            if (nebTool.isAdvancedMode == true)
            {
                DisplayAdvancedModeHelpBox();
            }
        }

        /// <summary>
        /// Lists all possible combinations of Source and Target fields conditions
        /// and display the help message to aid the user.
        /// </summary>
        private void DisplayGuideMessage()
        {
            if (isFieldNotNull == false)
            {
                EditorGUILayout.HelpBox("This is a tool to copy blendshapes between two models.\n" +
                                        "To get started, drag in your Source and Target models into these two fields", MessageType.Info);
                return;
            }

            if (isModelDifferent == false)
            {
                EditorGUILayout.HelpBox("Error! Source model and Target model are the exact same! \n" +
                                        "Please assign a different model to replace either of them.", MessageType.Warning);
                return;
            }

            if (isSourceFaceExist == false)
            {
                EditorGUILayout.HelpBox("Error! The Source Model doesn't have a Face child game object!\n" +
                                        "Make sure you drag in the model itself, not the Face gameobject!", MessageType.Warning);
                return;
            }

            if (isTargetFaceExist == false)
            {
                EditorGUILayout.HelpBox("Error! The Target Model doesn't have a Face child game object!\n" +
                                        "Make sure you drag in the model itself, not the Face gameobject!", MessageType.Warning);
                return;
            }

            if (isSourceSkinnedMeshExist == false)
            {
                EditorGUILayout.HelpBox("Error! The Source Model doesn't have a SkinnedMeshRenderer component on its Face gameobject!\n" +
                                        "Make sure you drag in a model that contains Face child gameobject with SkinnedMeshRenderer component!", MessageType.Warning);
                return;
            }

            if (isTargetSkinnedMeshExist == false)
            {
                EditorGUILayout.HelpBox("Error! The Target Model doesn't have a SkinnedMeshRenderer component on its Face gameobject!\n" +
                                        "Make sure you drag in a model that contains Face child gameobject with SkinnedMeshRenderer component!", MessageType.Warning);
                return;
            }

            if (isSourceMeshExist == false)
            {
                EditorGUILayout.HelpBox("Error! The Source SkinnedMeshRenderer component doesn't have any mesh assigned to it!\n" +
                                        "Please drag in a model that has the mesh assigned to it!", MessageType.Warning);
                return;
            }

            if (isTargetMeshExist == false)
            {
                EditorGUILayout.HelpBox("Error! The Target SkinnedMeshRenderer component doesn't have any mesh assigned to it!\n" +
                                        "Please drag in a model that has the mesh assigned to it!", MessageType.Warning);
                return;
            }

            if (isVertexCountMatched == false)
            {
                EditorGUILayout.HelpBox("Error! Vertex count mismatch between Source and Target models! \n\n" +
                                        "This is most likely because the model was exported from VRoid Studio with" +
                                        "\"Delete Transparent Meshes\" option checked. This option is enabled by default in the " +
                                        "\"Reduce Polygon\" export settings. Make sure to uncheck it and " +
                                        "export the model again into this Unity project.", MessageType.Warning);
                return;
            }

            EditorGUILayout.HelpBox("Alright! Click on the button to copy blendshapes", MessageType.Info);
        }

        private void DisplaySourceField()
        {
            EditorGUILayout.BeginHorizontal();

            if (isFieldNotNull == true)
            {
                //For normal mode:
                if (nebTool.isAdvancedMode == false)
                {
                    if (!isSourceMeshExist || !isSourceFaceExist || !isSourceSkinnedMeshExist ||
                        !isModelDifferent || !isVertexCountMatched)
                       GUI.color = colorWarning;
                }
                //For advanced mode
                else
                { 
                    if (!isSourceMeshExist || !isModelDifferent || !isVertexCountMatched)
                       GUI.color = colorWarning;
                }
            }

            if (nebTool.isAdvancedMode == false)
            {
                EditorGUILayout.LabelField("Source Model", GUILayout.Width(150f));
                nebTool.sourceModel = (GameObject)EditorGUILayout.ObjectField(nebTool.sourceModel, typeof(GameObject), true, GUILayout.ExpandWidth(true));
            }
            //On Advanced Mode, change the field to a general SkinnedMeshRender component
            else
            {
                EditorGUILayout.LabelField("Source Mesh Renderer", GUILayout.Width(150f));
                nebTool.sourceMeshRenderer = (SkinnedMeshRenderer)EditorGUILayout.ObjectField(nebTool.sourceMeshRenderer, typeof(SkinnedMeshRenderer), true, GUILayout.ExpandWidth(true));
            }

            GUI.color = Color.white;

            EditorGUILayout.EndHorizontal();
        }

        private void DisplayTargetField()
        {
            EditorGUILayout.BeginHorizontal();

            if (isFieldNotNull == true)
            {
                //For normal mode:
                if (nebTool.isAdvancedMode == false)
                {
                    if (!isTargetMeshExist || !isTargetFaceExist || !isTargetSkinnedMeshExist ||
                        !isModelDifferent || !isVertexCountMatched)
                        GUI.color = colorWarning;
                }
                //For advanced mode
                else
                {
                    if (!isTargetMeshExist || !isModelDifferent || !isVertexCountMatched)
                        GUI.color = colorWarning;
                }
            }

            if (nebTool.isAdvancedMode == false)
            {
                EditorGUILayout.LabelField("Target Model", GUILayout.Width(150f));
                nebTool.targetModel = (GameObject)EditorGUILayout.ObjectField(nebTool.targetModel, typeof(GameObject), true, GUILayout.ExpandWidth(true));
            }
            //On Advanced Mode, change the field to a general SkinnedMeshRender component
            else
            {
                EditorGUILayout.LabelField("Target Mesh Renderer", GUILayout.Width(150f));
                nebTool.targetMeshRenderer = (SkinnedMeshRenderer)EditorGUILayout.ObjectField(nebTool.targetMeshRenderer, typeof(SkinnedMeshRenderer), true, GUILayout.ExpandWidth(true));
            }

            GUI.color = Color.white;

            EditorGUILayout.EndHorizontal();
        }

        /// <summary>
        /// Updates the current field validation variables.
        /// These variables can then be used by Guide Message.
        /// </summary>
        private void FieldValidation()
        {
            //Optimization: Don't do any checks when there is no change in the Source and Target fields
            if (CheckForUpdatedFields() == false) return;

            //Set everything back to default true. Mostly for color notification.
            isFieldNotNull = true;
            isSourceFaceExist = true;
            isTargetFaceExist = true;
            isSourceSkinnedMeshExist = true;
            isTargetSkinnedMeshExist = true;
            isSourceMeshExist = true;
            isTargetMeshExist = true;
            isModelDifferent = true;
            isVertexCountMatched = true;



            //For advance mode and not advance mode
            GameObject sourceModel = null, targetModel = null;
            if(nebTool.isAdvancedMode == false)
            {
                sourceModel = nebTool.sourceModel;
                targetModel = nebTool.targetModel;
            }
            else
            {
                if(nebTool.sourceMeshRenderer != null) 
                    sourceModel = nebTool.sourceMeshRenderer.gameObject;
                if(nebTool.targetMeshRenderer != null) 
                    targetModel = nebTool.targetMeshRenderer.gameObject;
            }


            //Check if the Source and Target fields are filled
            isFieldNotNull = (sourceModel != null) && (targetModel != null);
            if (isFieldNotNull == false) return;

            //Check if the the Source and Target model are different objects
            if (CheckIsModelDifferent(sourceModel, targetModel) == false)
            {
                isModelDifferent = false;
                return;
            }
            isModelDifferent = true;



            //JUST FOR BASIC MODE
            if (nebTool.isAdvancedMode == false)
            {
                //Check if the Source model has a Face gameobject
                Transform sourceFace = sourceModel.transform.Find("Face");
                if (sourceFace == null)
                {
                    isSourceFaceExist = false;
                    return;
                }
                isSourceFaceExist = true;

                //Check if the Target model has a Face gameobject
                Transform targetFace = targetModel.transform.Find("Face");
                if (targetFace == null)
                {
                    isTargetFaceExist = false;
                    return;
                }
                isTargetFaceExist = true;

                //Check if the Source's Face has a SkinnedMeshRenderer component
                nebTool.sourceMeshRenderer = sourceFace.GetComponent<SkinnedMeshRenderer>();
                if (nebTool.sourceMeshRenderer == null)
                {
                    isSourceSkinnedMeshExist = false;
                    return;
                }
                isSourceSkinnedMeshExist = true;

                //Check if the Target's Face has a SkinnedMeshRenderer component
                nebTool.targetMeshRenderer = targetFace.GetComponent<SkinnedMeshRenderer>();
                if (nebTool.targetMeshRenderer == null)
                {
                    isTargetSkinnedMeshExist = false;
                    return;
                }
                isTargetSkinnedMeshExist = true;
            }
            //--- END OF JUST FOR BASIC MODE



            //Check if the Source Mesh exists in SkinnedMeshRenderer component
            nebTool.sourceMesh = nebTool.sourceMeshRenderer.sharedMesh;
            if (nebTool.sourceMesh == null)
            {
                isSourceMeshExist = false;
                return;
            }
            isSourceMeshExist = true;

            //Check if the Target Mesh exists in SkinnedMeshRenderer component
            nebTool.targetMesh = nebTool.targetMeshRenderer.sharedMesh;
            if (nebTool.targetMesh == null)
            {
                isTargetMeshExist = false;
                return;
            }
            isTargetMeshExist = true;

            //Check for the vertex count mismatch between Source and Target model
            isVertexCountMatched = (nebTool.sourceMesh.vertexCount == nebTool.targetMesh.vertexCount);
        }

        private void DisplayButton()
        {
            bool validCheck;
            if (nebTool.isAdvancedMode == false)
            {
                validCheck = isFieldNotNull && isSourceFaceExist &&
                             isTargetFaceExist && isSourceSkinnedMeshExist &&
                             isTargetSkinnedMeshExist && isModelDifferent && isVertexCountMatched;
            }
            else
            {
                validCheck = isFieldNotNull && isSourceMeshExist && isTargetMeshExist &&
                             isModelDifferent && isVertexCountMatched;
            }

            EditorGUI.BeginDisabledGroup(!validCheck);
            {
                if (GUILayout.Button("Copy Blendshapes", GUILayout.Height(50)))
                {
                    nebTool.CopyBlendshape();
                }
            }
            EditorGUI.EndDisabledGroup();
        }

        #region Advanced Mode Functions
        private void DisplayAdvancedToggle()
        {
            EditorGUILayout.BeginHorizontal();

            GUIContent labelTooltip = new GUIContent("Advanced Mode", "Unlock this tool to transfer any SkinnedMeshRenderer's blendshapes");
            EditorGUILayout.LabelField(labelTooltip, GUILayout.Width(150f));
            nebTool.isAdvancedMode = EditorGUILayout.Toggle(nebTool.isAdvancedMode, GUILayout.ExpandWidth(true));

            EditorGUILayout.EndHorizontal();
        }

        /// <summary>
        /// Lists all possible combinations of Source and Target fields conditions
        /// and display the help message to aid the user.
        /// </summary>
        private void DisplayGuideMessage_AdvancedMode()
        {
            if (isFieldNotNull == false)
            {
                EditorGUILayout.HelpBox("This is a tool to copy blendshapes between two SkinnedMeshRenderer components. \n" +
                                        "To get started, drag in your Source and Target SkinnedMeshRenderer into these two fields", MessageType.Info);
                return;
            }

            if (isModelDifferent == false)
            {
                EditorGUILayout.HelpBox("Error! Source Mesh and Target Mesh are the exact same! \n" +
                                        "Please assign a different SkinnedMeshRenderer to replace either of them.", MessageType.Warning);
                return;
            }

            if (isSourceMeshExist == false)
            {
                EditorGUILayout.HelpBox("Error! The Source SkinnedMeshRenderer component doesn't have any mesh assigned to it!\n" +
                                        "Please drag in a model that has the mesh assigned to it!", MessageType.Warning);
                return;
            }

            if (isTargetMeshExist == false)
            {
                EditorGUILayout.HelpBox("Error! The Target SkinnedMeshRenderer component doesn't have any mesh assigned to it!\n" +
                                        "Please drag in a model that has the mesh assigned to it!", MessageType.Warning);
                return;
            }

            if (isVertexCountMatched == false)
            {
                EditorGUILayout.HelpBox("Error! Vertex count mismatch between Source and Target models! \n\n" +
                                        "Please make sure you're dragging in similar models.", MessageType.Warning);
                return;
            }

            EditorGUILayout.HelpBox("Alright! Click on the button to copy blendshapes", MessageType.Info);
        }

        private void DisplayAdvancedModeHelpBox()
        {
            EditorGUILayout.HelpBox("Advanced Mode active. You can now use this tool to transfer blendshapes between any SkinnedMeshRenderer components.", MessageType.Info);
        }
        #endregion

        #region Helper Functions
        /// <summary>
        /// Compare two gameobjects. This also compares if the same object is the 
        /// instanced model or asset model in the Project Window.
        /// </summary>
        /// <param name="model1"></param>
        /// <param name="model2"></param>
        /// <returns>True if the model is the same. Returns false otherwise.</returns>
        private bool CheckIsModelDifferent(GameObject model1, GameObject model2)
        {
            if (model1 == null || model2 == null)
            {
                return true;
            }

            if (model1 == model2)
            {
                return false;
            }

            string prefabAssetPath1 = PrefabUtility.GetPrefabAssetPathOfNearestInstanceRoot(model1);
            string prefabAssetPath2 = PrefabUtility.GetPrefabAssetPathOfNearestInstanceRoot(model2);

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
        #endregion

        #region Optimization Functions
        /// <summary>
        /// Optimization: checks if there are any changes in the Source and Target fields.
        /// </summary>
        /// <returns>True if there are changes in Source and Model fields. False otherwise.</returns>
        private bool CheckForUpdatedFields()
        {
            bool isUpdated = false;

            if (nebTool.isAdvancedMode == false)
            {
                if (nebTool.sourceModel != lastKnownSource || nebTool.targetModel != lastKnownTarget)
                {
                    isUpdated = true;
                    lastKnownSource = nebTool.sourceModel;
                    lastKnownTarget = nebTool.targetModel;
                }
            }
            else
            {
                if (nebTool.sourceMeshRenderer != lastKnownSource || nebTool.targetMeshRenderer != lastKnownTarget)
                {
                    isUpdated = true;
                    lastKnownSource = nebTool.sourceMeshRenderer;
                    lastKnownTarget = nebTool.targetMeshRenderer;
                }
            }

            return isUpdated;
        }
        #endregion
    }
}
#endif