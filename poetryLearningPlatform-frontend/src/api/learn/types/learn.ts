export interface IWeightsData {
  weightsName: string
  weightsVersion: string
}

export interface ISwitchRoleRequestData {
  switchWeightsName: string
  switchWeightsVersion: string
}
export interface IPoetryContentData {
  poetryContent: string
}

// 定义响应回来数据格式-如果是对象则使用结构体去映射，是字符串则直接使用字符串
export type GetEnableWeightsResponseData = IApiResponseData<{ list: IWeightsData[] }>

export type GetGenerateWenXinTxtResponseData = IApiResponseData<{ poetryExplain: string }>

export type GetGeneratePlayPicResponseData = IApiResponseData<{ originalBase64: string }>

export type GetCurrentWeightsResponseData = IApiResponseData<IWeightsData>

export type SwitchWeightsResponseData = IApiResponseData<IWeightsData>

