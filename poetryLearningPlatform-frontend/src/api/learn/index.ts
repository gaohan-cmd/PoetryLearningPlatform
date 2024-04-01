import { request } from "@/utils/service"
import type * as Learn from "./types/learn"
import {GetGenerateMoellavaResponseData, IPoetryQuestionData} from "./types/learn";

/** 获取当前调用权重 */
export function getCurrentWeightsApi() {
  return request<Learn.GetCurrentWeightsResponseData>({
    url: "detect/weights/current",
    method: "get"
  })
}
/** 获取所有可调用权重 */
export function getAllEnableWeightsApi() {
  return request<Learn.GetEnableWeightsResponseData>({
    url: "detect/weights/list",
    method: "get"
  })
}

/** 文生图 */
export function generatePicByPlay(data: Learn.IPoetryContentData) {
  return request<Learn.GetGeneratePlayPicResponseData>({
    url: "chat/generate/playground",
    method: "post",
    data
  })
}

/** 文生文 */
export function generateTxtByWenXin(data: Learn.IPoetryContentData) {
  return request<Learn.GetGenerateWenXinTxtResponseData>({
    url: "chat/generate/wenxin",
    method: "post",
    data
  })
}

/** 图文问答 */
export function generateAnswerByMoellava(data: Learn.IPoetryQuestionData) {
  return request<Learn.GetGenerateMoellavaResponseData>({
    url: "chat/generate/moellava",
    method: "post",
    data
  })
}

/** 切换权重 */
export function switchWeightsApi(data: Learn.ISwitchRoleRequestData) {
  return request<Learn.SwitchWeightsResponseData>({
    url: "detect/weights/switch",
    method: "post",
    data
  })
}
