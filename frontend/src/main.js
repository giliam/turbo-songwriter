import Vue from 'vue'
import App from './App'
import VueTranslate from 'vue-translate-plugin';
import Vuex from 'vuex'
import {locales} from './common/locales.js'

Vue.use(Vuex);
Vue.use(VueTranslate);

Vue.locales(locales);

new Vue({
  el: '#app',
  router: require('./router').default,
  store: require('./store').default,
  template: '<App/>',
  components: { App }
})
