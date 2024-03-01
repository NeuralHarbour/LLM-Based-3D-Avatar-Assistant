using System;
using System.Collections.Generic;
using UnityEngine;
using UnityEditor;

using VRM;

public class VearDresser : EditorWindow
{
    private Transform targetAvatar = null;
    private Transform targetClothes = null;
    private bool transferBoneWeights = false;

    private Transform skeltonRoot = null;
    private SkinnedMeshRenderer skinnedMesh = null;


    [MenuItem("Tools/vear Dresser")]
    private static void ShowWindow()
    {
        var window = EditorWindow.GetWindow<VearDresser>();
        window.titleContent = new GUIContent("vear Dresser");
    }
 

    private void OnGUI()
    {
        using (var checkScope = new EditorGUI.ChangeCheckScope())
        {
            targetAvatar = EditorGUILayout.ObjectField("対象のアバター", targetAvatar, typeof(Transform), true) as Transform;
            targetClothes = EditorGUILayout.ObjectField("重ね着する衣装", targetClothes, typeof(Transform), true) as Transform;

            bool skeltonValidation = true;
            if (targetAvatar != null && targetClothes != null)
            {
                skeltonRoot = targetAvatar.Find("Root");
                skinnedMesh = targetClothes.Find("Body").GetComponent<SkinnedMeshRenderer>();

                List<Transform> avatarBones = new List<Transform>(targetAvatar.Find("Body").GetComponent<SkinnedMeshRenderer>().bones);
                List<Transform> clothesBones = new List<Transform>(skinnedMesh.bones);

                foreach (var e1 in clothesBones)
                {
                    bool find = false;
                    foreach (var e2 in avatarBones)
                    {
                        if (e1.name == e2.name)
                        {
                            find = true;
                            break;
                        }
                    }
                    if (!find) { skeltonValidation = false; }
                }
            }
            else
            {
                skeltonValidation = false;
            }

            EditorGUI.BeginDisabledGroup(!skeltonValidation);
            transferBoneWeights = EditorGUILayout.Toggle("ウェイトを転送する", transferBoneWeights);
            if (skeltonValidation)
            {
                EditorGUILayout.HelpBox("アバターと対象のスキンメッシュのスケルトン構造が一致しているため、ウェイト転送オプションが使用できます。ウェイト転送は、ボーンを増やさずに重ね着ができるオプション機能です。", MessageType.Info);
            }
            EditorGUI.EndDisabledGroup();
            if (!skeltonValidation && transferBoneWeights)
            {
                transferBoneWeights = false;
            }

            EditorGUILayout.Space();
            EditorGUI.BeginDisabledGroup(targetAvatar == null || targetClothes == null);
            if (GUILayout.Button("着用"))
            {
                if (PrefabUtility.IsAnyPrefabInstanceRoot(targetAvatar.gameObject) || PrefabUtility.IsAnyPrefabInstanceRoot(skinnedMesh.transform.root.gameObject))
                {
                    if (EditorUtility.DisplayDialog("確認", "対象のアバターと衣装のPrefabを解除してもよろしいですか？", "OK", "キャンセル"))
                    {
                        if (PrefabUtility.IsAnyPrefabInstanceRoot(targetAvatar.gameObject))
                        {
                            PrefabUtility.UnpackPrefabInstance(targetAvatar.gameObject, PrefabUnpackMode.Completely, InteractionMode.AutomatedAction);
                        }
                        if (PrefabUtility.IsAnyPrefabInstanceRoot(targetClothes.gameObject))
                        {
                            PrefabUtility.UnpackPrefabInstance(targetClothes.gameObject, PrefabUnpackMode.Completely, InteractionMode.AutomatedAction);
                        }
                    }
                }

                if (transferBoneWeights)
                {
                    TransferBoneWeights();
                }
                else
                {
                    TransferJoints();
                }

                targetAvatar = null;
                targetClothes = null;
            }
            EditorGUI.EndDisabledGroup();
        }
    }

    /// <summary>
    /// ウェイト転送方式
    /// </summary>
    private void TransferBoneWeights()
    {
        Transform[] childrens = targetAvatar.GetComponentsInChildren<Transform>(true);
        Transform[] bones = new Transform[skinnedMesh.bones.Length];
        for (int i = 0; i < skinnedMesh.bones.Length; i++)
        {
            bones[i] = Array.Find<Transform>(childrens, c => c.name == skinnedMesh.bones[i].name);
        }
        skinnedMesh.bones = bones;

        skinnedMesh.transform.localPosition = Vector3.zero;
        skinnedMesh.transform.localRotation = Quaternion.identity;
        skinnedMesh.transform.localScale = Vector3.one;

        CleanUp();
    }


    /// <summary>
    /// ボーン転送方式
    /// </summary>
    private void TransferJoints()
    {
        var clothesReference = skinnedMesh.rootBone;

        Transform[] bodyBones = GetAll(targetAvatar);
        Transform[] clothesBones = GetInfluenceBones(skinnedMesh.rootBone, skinnedMesh);// GetAll(clothesReference);

        List<Transform> b1 = new List<Transform>(clothesBones);
        List<Transform> b2 = new List<Transform>(skinnedMesh.rootBone.GetComponentsInChildren<Transform>());

        // 同名のボーンを探索し、発見したら同名のボーンの直下に配置
        for (int i = 0; i < clothesBones.Length; i++)
        {
            for (int j = 0; j < bodyBones.Length; j++)
            {
                var clothesBone = clothesBones[i];
                var bodyBone = bodyBones[j];
                if (clothesBone.name == bodyBone.name)
                {
                    clothesBone.SetParent(bodyBone.transform);
                    clothesBone.name = "Ex_" + clothesBone.name;    // Prefix追加

                    clothesBone.localPosition = Vector3.zero;
                    clothesBone.localRotation = Quaternion.identity;
                    clothesBone.localScale = Vector3.one;
                    break;
                }
            }
        }

        // 不要なボーンを全て削除
        foreach (var e in b2)
        {
            for (int i = 0; i < e.childCount; i++)
            {
                e.GetChild(i).SetParent(e.parent);
            }
        }
        foreach (var e in b2)
        {
            if (!b1.Contains(e))
            {
                DestroyImmediate(e.gameObject);
            }
        }

        var secondary1 = targetAvatar.Find("secondary");
        var secondary2 = targetClothes.Find("secondary");

        VRMSpringBone[] vrmSpringBones = secondary2.GetComponents<VRMSpringBone>();

        foreach(var e in vrmSpringBones)
        {
            if (e.RootBones.Count > 0)
            {
                var sb = secondary1.gameObject.AddComponent<VRMSpringBone>();
                sb.m_comment = e.m_comment;
                sb.m_stiffnessForce = e.m_stiffnessForce;
                sb.m_gravityPower = e.m_gravityPower;
                sb.m_gravityDir = e.m_gravityDir;
                sb.m_dragForce = e.m_dragForce;
                sb.m_center = skeltonRoot;  //e.m_center;
                sb.RootBones = e.RootBones;
                sb.m_hitRadius = e.m_hitRadius;
                sb.ColliderGroups = e.ColliderGroups;
                sb.m_updateType = e.m_updateType;
            }
        }

        CleanUp();
    }


    /// <summary>
    /// 転送後の最終処理
    /// </summary>
    private void CleanUp()
    {
        targetClothes.SetParent(targetAvatar);
        GameObject clothes = new GameObject("Clothes");
        clothes.transform.SetParent(targetAvatar);

        skinnedMesh.transform.SetParent(clothes.transform);
        skinnedMesh.rootBone = skeltonRoot;

        var secondary = targetClothes.Find("secondary");
        DestroyImmediate(secondary.gameObject);
        //secondary.SetParent(clothes.transform);

        var face = targetClothes.Find("Face");
        var hair = targetClothes.Find("Hair");
        if (face != null) { DestroyImmediate(face.gameObject); }
        if (hair != null) { DestroyImmediate(hair.gameObject); }

        DestroyImmediate(targetClothes.gameObject);

        // T-Poseにノーマライズ
        VRMBoneNormalizer.Execute(targetAvatar.gameObject, true);
        DestroyImmediate(targetAvatar.gameObject);
    }

    /// <summary>
    /// SkinnedMeshに影響するボーンを取得
    /// </summary>
    private Transform[] GetInfluenceBones(Transform root, SkinnedMeshRenderer skinnedMesh)
    {
        List<Transform> bindedBones = new List<Transform>();
        var b = skinnedMesh.sharedMesh.GetAllBoneWeights();
        foreach (var e in b)
        {
            var bone = skinnedMesh.bones[e.boneIndex];
            if (!bindedBones.Contains(bone))
            {
                bindedBones.Add(bone);
            }
        }
        return bindedBones.ToArray();
    }

    private Transform[] GetAll(Transform obj)
    {
        List<Transform> allChildren = new List<Transform>();
        GetChildren(obj, ref allChildren);
        return allChildren.ToArray();
    }

    private void GetChildren(Transform obj, ref List<Transform> allChildren)
    {
        Transform children = obj.GetComponentInChildren<Transform>();
        //子要素がいなければ終了
        if (children.childCount == 0)
        {
            return;
        }
        foreach (Transform ob in children)
        {
            allChildren.Add(ob);
            GetChildren(ob, ref allChildren);
        }
    }
}