<script lang="ts" setup>
import { generateTxtByWenXin } from "@/api/learn"
import { ref } from "vue"

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

const getGenerateTxtByWenXin = async (inputText: string) => {
  loading.value = true
  try {
    const response = await generateTxtByWenXin({ poetryContent: inputText })
    poetryExplain.value = JSON.stringify(response.data.poetryExplain)
  } catch (error) {
    poetryExplain.value = "请求失败，请重试"
    console.error(error)
  } finally {
    loading.value = false
  }
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
            <el-button type="primary" @click="handleConfirm">确认</el-button>
          </div>
        </el-col>
        <el-col :span="24">
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
