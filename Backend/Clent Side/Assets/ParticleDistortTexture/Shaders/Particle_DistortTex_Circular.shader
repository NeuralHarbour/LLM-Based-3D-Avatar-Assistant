// Upgrade NOTE: replaced 'mul(UNITY_MATRIX_MVP,*)' with 'UnityObjectToClipPos(*)'

Shader "Particle Distort Texture/Circular" 
{
Properties 
{
	[Enum(Off,0,Front,1,Back,2)] _CullMode ("Culling Mode", int) = 0
	[Enum(Additive,1,AlphaBlend,10)] _DstBlend ("Desination Blend Options", Int) = 1
	_DistortX ("Distortion in X", Range (0,2)) = 1
	_DistortY ("Distortion in Y", Range (0,2)) = 0
	_MaskTex ("_MaskTex A", 2D) = "white" {}
	_Distort ("_Distort A", 2D) = "white" {}
	_MainTex ("_MainTex RGBA", 2D) = "white" {}
	_AlphaM ("Alpha Multiplier", Range (0,10)) = 1
}

Category 
{
	Tags { "Queue"="Transparent" "IgnoreProjector"="True" "RenderType"="Transparent" }
	Blend SrcAlpha [_DstBlend]
	Cull [_CullMode] Lighting Off ZWrite Off

	Lighting Off
	
	SubShader 
	{
		Pass 
		{
		
			CGPROGRAM
			#pragma vertex vert
			#pragma fragment frag

			#include "UnityCG.cginc"

			sampler2D _MainTex;
			sampler2D _Distort;
			sampler2D _MaskTex;
			
			struct appdata_t 
			{
				fixed4 vertex : POSITION;
				fixed2 texcoord : TEXCOORD0;
				fixed4 color : COLOR;
			};

			struct v2f 
			{
				fixed4 vertex : SV_POSITION;
				fixed2 texcoord : TEXCOORD0;
				fixed2 texcoord1 : TEXCOORD1;
				fixed4 color : COLOR;
			};
			
			fixed4 _MainTex_ST;
			fixed4 _Distort_ST;
			fixed4 _MaskTex_ST;
			
			fixed _DistortX;
			fixed _DistortY;
			fixed _AlphaM;

			v2f vert (appdata_t v)
			{
				v2f o;
				o.vertex = UnityObjectToClipPos(v.vertex);
				o.texcoord = TRANSFORM_TEX(v.texcoord,_Distort);
				o.texcoord1 = v.texcoord;
				o.color = v.color;
				return o;
			}
			
			fixed4 frag (v2f i) : Color
			{
				fixed tex = tex2D(_MaskTex, i.texcoord1).a;
				fixed distort = tex2D(_Distort, i.texcoord).a;
				
				fixed2 distortUV = fixed2((
									i.texcoord1.x/tex //x UV
									-distort)*_DistortX,(
									i.texcoord1.y/tex //y UV
									-distort)*_DistortY);
									
				fixed4 tex2 = tex2D(_MainTex,distortUV);
				return fixed4(tex2.rgb,tex2.a*tex*_AlphaM)*i.color;
			}
			ENDCG 
		}
	}	
}
}
