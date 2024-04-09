<template>
  <div>
    <div v-for="collection in collections" :key="collection.c_id">
      <n-card
        title=""
        style="padding: 1rem; margin-top: 1rem"
        @click="
          () => {
            this.view_collection_poems(collection.c_id)
          }
        "
      >
        <n-h2>{{ collection.c_name }}</n-h2>
        <n-p>{{ collection.c_note }}</n-p>
        <!-- 将按钮放置在 n-card 的内容区域之外 -->
      </n-card>
      <!-- 在 n-card 外部添加按钮 -->
      <n-button class="button-generate-cloud" @click="generate_cloud(collection.c_id)">词云生成</n-button>
    </div>
  </div>
</template>

<script>
import { defineComponent } from "vue"
import { NCard, NH2, NP } from "naive-ui"
import axios from "axios"
import router from "../../../router/index.ts"
export default defineComponent({
  name: "Collection",
  components: {
    NCard,
    NH2,
    NP
  },
  methods: {
    view_collection_poems: function (id) {
      router.push("/search_poem_other_list/collection/" + id)
    },
    generate_cloud: function (id) {
      router.push("/poem/cloud/collection/" + id)
    }
  },
  mounted() {
    axios
      .get(this.BASE_URL + "/display/collection")
      .then((response) => {
        this.collections = response.data
        this.ready_render = true
      })
      .catch(function (error) {
        console.log(error)
      })
  },
  data() {
    return {
      ready_render: false,
      collections: []
    }
  },
  setup() {
    return {}
  },
  props: {}
})
</script>

<style scoped>
.n-card:hover {
  transition-duration: 0.7s;
  border-color: #18a058;
  cursor: pointer;
}
.button-generate-cloud {
  background-color: #008cba; /* 设置按钮的背景色 */
  color: white; /* 设置按钮的文字颜色 */
  border: none; /* 移除按钮边框 */
  padding: 0.5rem 1rem; /* 设置按钮内边距 */
  border-radius: 4px; /* 设置按钮圆角 */
  cursor: pointer; /* 将鼠标光标设置为指针 */
  transition: background-color 0.3s ease; /* 添加背景色过渡效果 */
}

.button-generate-cloud:hover {
  background-color: #005f7f; /* 设置鼠标悬停时按钮的背景色 */
}
</style>
