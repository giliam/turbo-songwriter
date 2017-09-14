import Vue from 'vue'
import Vuex from 'vuex'
import VueTranslate from 'vue-translate-plugin';
import VueSession from 'vue-session'

import App from './App'
import {locales} from './common/locales.js'

Vue.use(Vuex);
Vue.use(VueTranslate);
Vue.use(VueSession)

Vue.locales(locales);

new Vue({
  el: '#app',
  router: require('./router').default,
  store: require('./store').default,
  template: '<App/>',
  components: { App }
})
