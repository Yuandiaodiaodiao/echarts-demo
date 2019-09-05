import Vue from 'vue'
import App from './App.vue'
import router from './router'
import echarts from 'echarts'
import 'echarts/extension/bmap/bmap'
import Element from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'
import axios from 'axios'
import configs from './config/config'
Vue.config.productionTip = false
Vue.prototype.$echarts = echarts
axios.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded'
axios.defaults.crossDomain = true
Vue.prototype.axios = axios
Vue.use(Element, { size: 'small', zIndex: 3000 })
Vue.prototype.config_const = {
  api_url: 'http://'+configs.ip+':'+configs.port
}
new Vue({
  router,
  render: h => h(App)
}).$mount('#app')
