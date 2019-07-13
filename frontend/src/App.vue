<template>
  <el-row>
    <el-container>
      <el-header style="text-align:middle;font-size: 25px">欢迎使用在线手写签名系统</el-header>
      <el-container>
        <el-aside width="200px" style="background-color: rgb(238, 241, 246)">
          <el-menu :default-openeds="['1', '3']">
            <el-submenu index="1">
              <template slot="title">
                <i class="el-icon-message"></i>导航栏
              </template>
              <el-menu-item-group>
                <el-menu-item
                  index="1-1"
                  onclick="window.frames['bdIframe'].src='/static/login.html'"
                >登陆</el-menu-item>
                <el-menu-item
                  index="1-2"
                  onclick="window.frames['bdIframe'].src='/static/register.html'"
                >注册</el-menu-item>
                <el-menu-item
                  index="1-3"
                  onclick="window.frames['bdIframe'].src='/static/update.html'"
                >识别优化</el-menu-item>
              </el-menu-item-group>
            </el-submenu>
            <el-submenu index="2">
              <template slot="title">
                <i class="el-icon-menu"></i>产品说明
              </template>
              <el-menu-item-group>
                <el-menu-item index="2-1">官方文档</el-menu-item>
                <el-menu-item index="2-2">购买产品</el-menu-item>
                <el-menu-item index="2-2">检查更新</el-menu-item>
              </el-menu-item-group>
            </el-submenu>
            <el-submenu index="3">
              <template slot="title">
                <i class="el-icon-setting"></i>联系我们
              </template>
              <el-menu-item-group>
                <el-menu-item index="3-1">gmail</el-menu-item>
                <el-menu-item index="3-2">telephone</el-menu-item>
                <el-menu-item
                  index="3-2"
                  onclick="location.href='https://github.com/w1ndseek2/HWRR'"
                >github</el-menu-item>
              </el-menu-item-group>
            </el-submenu>
          </el-menu>
        </el-aside>
        <el-main>
          <iframe
            ref="iframe"
            id="bdIframe"
            src="/api/index"
            frameborder="0"
            scrolling="auto"
          ></iframe>
        </el-main>
      </el-container>
    </el-container>
  </el-row>
</template>

<script>
export default {
  data () {
    return {
      bdTokenUrl: ''
    }
  },
  created () {
    this.getUrl()
    this.$nextTick(() => {
      this.getCode()
    })
  },
  mounted () {
    /**
     * iframe-宽高自适应显示
     */
    const oIframe = document.getElementById('bdIframe')
    const deviceWidth = document.documentElement.clientWidth
    const deviceHeight = document.documentElement.clientHeight
    oIframe.style.width = Number(deviceWidth) - 330 + 'px' // 数字是页面布局宽度差值
    oIframe.style.height = Number(deviceHeight) - 130 + 'px' // 数字是页面布局高度差
  },
  methods: {
    /**
     * 获取-外部接口信息
     */
    getUrl () {
      let that = this
      let bdUrl = { queryurl: this.$paths.bdpath + '/locate' }
      this.$api.getBdToken(bdUrl, function (res) {
        that.bdTokenUrl = res.data.data
      })
    }
  }
}
</script>

<style>
#app {
  font-family: "Avenir", Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
