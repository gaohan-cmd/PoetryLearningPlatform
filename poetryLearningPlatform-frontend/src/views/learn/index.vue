<script lang="ts" setup>
import { generatePicByPlay, generateTxtByWenXin } from "@/api/learn"
import { computed, reactive, ref } from "vue"

defineOptions({
  name: "Learn"
})
const inputValue = ref("")
const poetryExplain = ref("")
const loading = ref(false)
/** 获取文心一言回答 */
const handleConfirm = () => {
  if (inputValue.value) {
    getGenerateTxtByWenXin(inputValue.value)
  } else {
    // 输入为空的处理逻辑
  }
}
/** 获取文生成图片 */
const handleImage = () => {
  if (inputValue.value) {
    getGeneratePicByPlay(inputValue.value)
  } else {
    // 输入为空的处理逻辑
  }
}

const getGenerateTxtByWenXin = async (inputText: string) => {
  loading.value = true
  try {
    const response = await generateTxtByWenXin({ poetryContent: inputText })
    poetryExplain.value = response.data.poetryExplain.replace(/\\n/g, "\n").slice(0, -1)
  } catch (error) {
    poetryExplain.value = "请求失败，请重试"
    console.error(error)
  } finally {
    loading.value = false
  }
}

// 诗词生成图片
// 检测结果图片
// base64解码
const detectImageData: any = reactive({
  originalBase64: "",
  resultBase64: "",
  originalImageUrl: computed(() => {
    if (detectImageData.originalBase64) {
      const blob = dataURItoBlob(detectImageData.originalBase64)
      return URL.createObjectURL(blob)
    } else {
      return ""
    }
  }),
  detectResult: []
})
// 文生图片生成
const getGeneratePicByPlay = async (inputText: string) => {
  const res = await generatePicByPlay({ poetryContent: inputText })
  // 如果后端的数据没有以 data:image/jpeg;base64 则需要判断加上
  const originalBase64 = res.data.originalBase64
  const base64Prefix = "data:image/jpeg;base64,"
  // 判断 originalBase64 是否以 base64Prefix 开头，如果没有则加上
  if (!originalBase64.startsWith(base64Prefix)) {
    detectImageData.originalBase64 = base64Prefix + originalBase64
  } else {
    detectImageData.originalBase64 = originalBase64
  }
}
// 图片base64解码
const dataURItoBlob = (dataURI: any) => {
  const byteString = atob(dataURI.split(",")[1])
  const mimeString = dataURI.split(",")[0].split(":")[1].split(";")[0]
  const ab = new ArrayBuffer(byteString.length)
  const ia = new Uint8Array(ab)
  for (let i = 0; i < byteString.length; i++) {
    ia[i] = byteString.charCodeAt(i)
  }
  return new Blob([ab], { type: mimeString })
}
</script>

<template>
  <div class="app-container">
    <el-card v-loading="loading" shadow="never" class="search-wrapper">
      <el-row>
        <el-col :span="24">
          <div class="input-wrapper">
            <el-input
              v-model="inputValue"
              placeholder="请输入您需要问答的诗词"
              prefix-icon="el-icon-edit-outline"
              clearable
              class="poetry-input"
            />
            <el-button type="primary" @click="handleConfirm">诗词赏析</el-button>
            <el-button type="primary" @click="handleImage">图像生成</el-button>
          </div>
        </el-col>
      </el-row>
    </el-card>
    <el-card v-loading="loading" shadow="never" class="search-wrapper">
      <el-row :gutter="20">
        <el-col :span="10">
          <div class="grid-content ep-bg-purple">
            <el-image
              v-if="detectImageData.originalBase64"
              :src="detectImageData.originalImageUrl"
              :fit="'scaleDown'"
              :preview-src-list="[detectImageData.originalImageUrl]"
            />
            <div v-else class="image-placeholder">原始图片</div>
          </div>
        </el-col>
        <el-col :span="10">
          <el-input type="textarea" autosize v-model="poetryExplain" class="response-textarea" readonly />
        </el-col>
      </el-row>
    </el-card>
  </div>
</template>

<style lang="scss" scoped>
.image-placeholder {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100%;
  height: 300px;
  background: var(--el-fill-color-light);
  color: var(--el-text-color-secondary);
  font-size: 15px;
}
.el-row {
  margin-bottom: 20px;
}
.el-row:last-child {
  margin-bottom: 0;
}
.el-col {
  border-radius: 4px;
}
.grid-content {
  border-radius: 4px;
  min-height: 36px;
}
.SwitchModelCSS {
  display: flex;
  font-size: 15px;
  font-weight: 500;
  padding: 5px;
  justify-content: flex-start;
  align-items: center;
}
.search-wrapper {
  margin-bottom: 20px;
  :deep(.el-card__body) {
    padding-bottom: 15px;
  }
}
.toolbar-wrapper {
  display: flex;
  justify-content: space-between;
  margin-bottom: 20px;
}
.table-wrapper {
  margin-bottom: 20px;
}
.pager-wrapper {
  display: flex;
  justify-content: flex-end;
}

.input-wrapper {
  display: flex;
  align-items: center;
}

.poetry-input {
  flex: 1;
  margin-right: 10px;
}

.response-textarea {
  margin-top: 10px;
}
</style>
