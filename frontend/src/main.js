import Vue from 'vue'
import router from './router'
import App from './App'
import VueTranslate from 'vue-translate-plugin';
import {locales} from './common/locales.js'

Vue.use(VueTranslate);

Vue.locales(locales);

new Vue({
  el: '#app',
  router,
  template: '<App/>',
  components: { App }
})
