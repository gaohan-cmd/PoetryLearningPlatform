<template>
  <div class="container">
    <div class="search-container">
      <el-select v-model="query_option" placeholder="选择查询方式">
        <el-option v-for="item in options" :key="item.value" :label="item.label" :value="item.value" />
      </el-select>
      <el-input v-model="query_text" placeholder="信息" clearable />
      <el-button type="primary" @click="search">查询</el-button>
    </div>
    <div class="image-container">
      <img src="/DSC07440.jpg" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue"
import { ElButton, ElInput, ElOption, ElSelect, ElMessage } from "element-plus"
import { useRouter } from "vue-router"
const router = useRouter()
defineOptions({
  name: "Search"
})

const query_option = ref("title")
const query_text = ref("")
const options = [
  { label: "标题", value: "title" },
  { label: "正文", value: "para" },
  { label: "词牌/韵律", value: "rhy" },
  { label: "作者", value: "author" }
]

const createMessage = () => {
  ElMessage.warning("查询内容不能为空")
}

const search = () => {
  if (!query_text.value) {
    createMessage()
  } else {
    router.push(`/poem/search_poem_list/${query_option.value}/${query_text.value}`)
  }
}
</script>

<style scoped>
.container {
  display: flex;
  flex-direction: column;
  align-items: center;
  max-width: 70%;
  margin: 8% auto;
  padding: 1rem;
}

.search-container {
  display: flex;
  justify-content: center;
  gap: 1rem;
}

.image-container {
  max-width: 500px;
  margin-top: 4rem;
}

img {
  max-width: 100%;
  height: auto;
  width: auto\9;
}
</style>
