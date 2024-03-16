export interface IWeightsData {
  weightsName: string
  weightsVersion: string
}

export interface ISwitchRoleRequestData {
  switchWeightsName: string
  switchWeightsVersion: string
}

// 传递的参数-需要和后端对应
export interface IPoetryExplainData {
  poetryContent: string
}

export type GetEnableWeightsResponseData = IApiResponseData<{ list: IWeightsData[] }>

export type GetGenerateWenXinTxtResponseData = IApiResponseData<{ poetryExplain: IPoetryExplainData[] }>

export type GetCurrentWeightsResponseData = IApiResponseData<IWeightsData>

export type SwitchWeightsResponseData = IApiResponseData<IWeightsData>
