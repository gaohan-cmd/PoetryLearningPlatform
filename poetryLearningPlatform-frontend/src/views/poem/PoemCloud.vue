<template>
  <section class="cloud-bed">
    <div class="cloud-box">
      <span
        v-for="(item, index) in dataList"
        :key="index"
        @click="getDataInfo(item)"
        :style="{ fontSize: item.size, color: item.color, backgroundColor: item.bgColor }"
      >
        {{ item.name }}
      </span>
    </div>
  </section>
  <!--  <div>-->
  <!--    <div class="wordcloud-container">-->
  <!--      &lt;!&ndash; echarts图表 &ndash;&gt;-->
  <!--      <wordcloud />-->
  <!--    </div>-->
  <!--  </div>-->
  <div class="wordcloud-container">
    <div id="chart" style="width: 500px; height: 400px" />
  </div>
</template>

<script>
import * as echarts from "echarts"
import "echarts-wordcloud"
export default {
  name: "word-cloud",
  props: {
    query_method: {
      type: String,
      default: ""
    },
    query_id: {
      type: String,
      default: ""
    }
  },
  data() {
    return {
      timer: 50,
      radius: 0,
      dtr: Math.PI / 180,
      active: false,
      lasta: 0.2,
      lastb: 0.5,
      distr: true,
      tspeed: 0,
      mouseX: 0,
      mouseY: 0,
      tagAttrList: [],
      tagContent: null,
      cloudContent: null,
      sinA: "",
      cosA: "",
      sinB: "",
      cosB: "",
      sinC: "",
      cosC: "",
      dataList: [
        // 保持原有的dataList内容或者按需更新
        {
          name: "页面卡顿白屏",
          value: "1"
        },
        {
          name: "闪退",
          value: "8"
        },
        {
          name: "登录问题",
          value: "9"
        },
        {
          name: "功能bug",
          value: "3"
        },
        {
          name: "无法收到短信",
          value: "6"
        },
        {
          name: "人脸/指纹认证失败",
          value: "10"
        },
        {
          name: "功能建议",
          value: "2"
        },
        {
          name: "UI/UX",
          value: "5"
        },
        {
          name: "导航性",
          value: "7"
        }
      ],
      wordList: [
        {
          name: "珍珠奶茶",
          value: 15000
        },
        {
          name: "冰激凌红茶",
          value: 10081
        },
        {
          name: "椰果奶茶",
          value: 9386
        },
        {
          name: "波霸奶茶",
          value: 7500
        },
        {
          name: "金桔柠檬",
          value: 7500
        },
        {
          name: "乌龙奶茶",
          value: 6500
        },
        {
          name: "芒果欧蕾",
          value: 6500
        },
        {
          name: "仙草奶茶",
          value: 6000
        },
        {
          name: "翡翠柠檬",
          value: 4500
        },
        {
          name: "芒果养乐多",
          value: 3800
        },
        {
          name: "柠檬养乐多",
          value: 3000
        },
        {
          name: "波霸奶绿",
          value: 2500
        },
        {
          name: "四季春茶",
          value: 2300
        },
        {
          name: "茉莉绿茶",
          value: 2000
        },
        {
          name: "阿萨姆红茶",
          value: 1900
        },
        {
          name: "奶冻摇摇乐",
          value: 1800
        },
        {
          name: "冻顶乌龙茶",
          value: 1700
        },
        {
          name: "咖啡",
          value: 1600
        },
        {
          name: "焦糖玛奇朵",
          value: 1500
        },
        {
          name: "金桔柠檬",
          value: 1200
        }
      ]
    }
  },
  mounted() {
    console.log("query_method--" + this.query_method)
    console.log("query_id--" + this.query_id)
    this.initchart()
    this.$nextTick(() => {
      this.radius = document.querySelector(".cloud-box").offsetWidth / 2
      this.dataList.forEach((item) => {
        item.size = `${parseInt(item.value) * 1.5 + 10}px` // 根据value调整大小
        item.color = this.randomColor() // 设置随机颜色
        item.bgColor = this.randomColorWithOpacity() // 设置随机背景颜色
      })
      this.initWordCloud()
    })
  },
  beforeUnmount() {
    clearInterval(this.timer)
  },
  methods: {
    getDataInfo(item) {
      console.log(item, "item")
    },
    initWordCloud() {
      this.cloudContent = document.querySelector(".cloud-box")
      this.tagContent = this.cloudContent.getElementsByTagName("span")
      for (let i = 0; i < this.tagContent.length; i++) {
        const tagObj = {}
        tagObj.offsetWidth = this.tagContent[i].offsetWidth
        tagObj.offsetHeight = this.tagContent[i].offsetHeight
        this.tagAttrList.push(tagObj)
      }
      this.sineCosine(0, 0, 0)
      this.positionAll()
      this.cloudContent.onmouseover = () => {
        this.active = true
      }
      this.cloudContent.onmouseout = () => {
        this.active = false
      }
      this.cloudContent.onmousemove = (ev) => {
        const oEvent = window.event || ev
        this.mouseX = oEvent.clientX - (this.cloudContent.offsetLeft + this.cloudContent.offsetWidth / 2)
        this.mouseY = oEvent.clientY - (this.cloudContent.offsetTop + this.cloudContent.offsetHeight / 2)
        this.mouseX /= 5
        this.mouseY /= 5
      }
      setInterval(this.update, this.timer)
    },
    positionAll() {
      let phi = 0
      let theta = 0
      const max = this.tagAttrList.length
      const aTmp = []
      const oFragment = document.createDocumentFragment()
      //随机排序
      for (let i = 0; i < this.tagContent.length; i++) {
        aTmp.push(this.tagContent[i])
      }
      aTmp.sort(() => {
        return Math.random() < 0.5 ? 1 : -1
      })
      for (let i = 0; i < aTmp.length; i++) {
        oFragment.appendChild(aTmp[i])
      }
      this.cloudContent.appendChild(oFragment)
      for (let i = 1; i < max + 1; i++) {
        if (this.distr) {
          phi = Math.acos(-1 + (2 * i - 1) / max)
          theta = Math.sqrt(max * Math.PI) * phi
        } else {
          phi = Math.random() * Math.PI
          theta = Math.random() * (2 * Math.PI)
        }
        //坐标变换
        this.tagAttrList[i - 1].cx = this.radius * Math.cos(theta) * Math.sin(phi)
        this.tagAttrList[i - 1].cy = this.radius * Math.sin(theta) * Math.sin(phi)
        this.tagAttrList[i - 1].cz = this.radius * Math.cos(phi)
        this.tagContent[i - 1].style.left =
          this.tagAttrList[i - 1].cx +
          this.cloudContent.offsetWidth / 2 -
          this.tagAttrList[i - 1].offsetWidth / 2 +
          "px"
        this.tagContent[i - 1].style.top =
          this.tagAttrList[i - 1].cy +
          this.cloudContent.offsetHeight / 2 -
          this.tagAttrList[i - 1].offsetHeight / 2 +
          "px"
      }
    },
    update() {
      let angleBasicA
      let angleBasicB

      if (this.active) {
        angleBasicA = (-Math.min(Math.max(-this.mouseY, -200), 200) / this.radius) * this.tspeed
        angleBasicB = (Math.min(Math.max(-this.mouseX, -200), 200) / this.radius) * this.tspeed
      } else {
        angleBasicA = this.lasta * 0.98
        angleBasicB = this.lastb * 0.98
      }

      //默认转动是后是否需要停下
      // lasta=a;
      // lastb=b;

      // if(Math.abs(a)<=0.01 && Math.abs(b)<=0.01)
      // {
      // return;
      // }
      this.sineCosine(angleBasicA, angleBasicB, 0)
      for (let j = 0; j < this.tagAttrList.length; j++) {
        const rx1 = this.tagAttrList[j].cx
        const ry1 = this.tagAttrList[j].cy * this.cosA + this.tagAttrList[j].cz * -this.sinA
        const rz1 = this.tagAttrList[j].cy * this.sinA + this.tagAttrList[j].cz * this.cosA

        const rx2 = rx1 * this.cosB + rz1 * this.sinB
        const ry2 = ry1
        const rz2 = rx1 * -this.sinB + rz1 * this.cosB

        const rx3 = rx2 * this.cosC + ry2 * -this.sinC
        const ry3 = rx2 * this.sinC + ry2 * this.cosC
        const rz3 = rz2
        this.tagAttrList[j].cx = rx3
        this.tagAttrList[j].cy = ry3
        this.tagAttrList[j].cz = rz3

        const per = 350 / (350 + rz3)

        this.tagAttrList[j].x = rx3 * per - 2
        this.tagAttrList[j].y = ry3 * per
        this.tagAttrList[j].scale = per
        this.tagAttrList[j].alpha = per

        this.tagAttrList[j].alpha = (this.tagAttrList[j].alpha - 0.6) * (10 / 6)
      }
      this.doPosition()
      this.depthSort()
    },
    doPosition() {
      const len = this.cloudContent.offsetWidth / 2
      const height = this.cloudContent.offsetHeight / 2
      for (let i = 0; i < this.tagAttrList.length; i++) {
        this.tagContent[i].style.left = this.tagAttrList[i].cx + len - this.tagAttrList[i].offsetWidth / 2 + "px"
        this.tagContent[i].style.top = this.tagAttrList[i].cy + height - this.tagAttrList[i].offsetHeight / 2 + "px"
        // this.tagContent[i].style.fontSize = Math.ceil(12 * this.tagAttrList[i].scale/2) + 8 + 'px';
        this.tagContent[i].style.fontSize = Math.ceil((12 * this.tagAttrList[i].scale) / 2) + 10 + "px"
        this.tagContent[i].style.filter = "alpha(opacity=" + 100 * this.tagAttrList[i].alpha + ")"
        this.tagContent[i].style.opacity = this.tagAttrList[i].alpha + 0.2
      }
    },
    depthSort() {
      const aTmp = []
      for (let i = 0; i < this.tagContent.length; i++) {
        aTmp.push(this.tagContent[i])
      }
      aTmp.sort((item1, item2) => item2.cz - item1.cz)
      for (let i = 0; i < aTmp.length; i++) {
        aTmp[i].style.zIndex = i
      }
    },
    sineCosine(a, b, c) {
      this.sinA = Math.sin(a * this.dtr)
      this.cosA = Math.cos(a * this.dtr)
      this.sinB = Math.sin(b * this.dtr)
      this.cosB = Math.cos(b * this.dtr)
      this.sinC = Math.sin(c * this.dtr)
      this.cosC = Math.cos(c * this.dtr)
    },
    randomColor() {
      return `#${Math.floor(Math.random() * 16777215).toString(16)}`
    },
    randomColorWithOpacity() {
      const opacity = Math.random().toFixed(2) // 随机透明度，范围在0到1之间
      return `rgba(${Math.floor(Math.random() * 256)}, ${Math.floor(Math.random() * 256)}, ${Math.floor(
        Math.random() * 256
      )}, ${opacity})`
    },
    initchart() {
      const myChart = echarts.init(document.querySelector("#chart"))
      myChart.setOption({
        series: [
          {
            type: "wordCloud",
            //用来调整词之间的距离
            gridSize: 10,
            //用来调整字的大小范围
            // Text size range which the value in data will be mapped to.
            // Default to have minimum 12px and maximum 60px size.
            sizeRange: [14, 60],
            // Text rotation range and step in degree. Text will be rotated randomly in range [-90,                                                                             90] by rotationStep 45
            //用来调整词的旋转方向，，[0,0]--代表着没有角度，也就是词为水平方向，需要设置角度参考注释内容
            // rotationRange: [-45, 0, 45, 90],
            // rotationRange: [ 0,90],
            rotationRange: [0, 0],
            //随机生成字体颜色
            // maskImage: maskImage,
            textStyle: {
              color: function () {
                return (
                  "rgb(" +
                  Math.round(Math.random() * 255) +
                  ", " +
                  Math.round(Math.random() * 255) +
                  ", " +
                  Math.round(Math.random() * 255) +
                  ")"
                )
              }
            },
            //位置相关设置
            // Folllowing left/top/width/height/right/bottom are used for positioning the word cloud
            // Default to be put in the center and has 75% x 80% size.
            left: "center",
            top: "center",
            right: null,
            bottom: null,
            width: "200%",
            height: "200%",
            //数据
            data: this.wordList
          }
        ]
      })
    }
  }
}
</script>

<style scoped>
.cloud-bed {
  width: 400px;
  height: 400px;
  margin: auto;
}
.cloud-box {
  position: relative;
  margin: 20px auto 0px;
  width: 100%;
  height: 100%;
  background: #00000000;
}
.cloud-box span {
  position: absolute;
  padding: 3px 6px;
  top: 0px;
  font-weight: bold;
  text-decoration: none;
  left: 0px;
  border-radius: 50%;
  text-align: center;

  display: flex;
  align-items: center;
  justify-content: center;
}
.wordcloud-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
}
</style>
