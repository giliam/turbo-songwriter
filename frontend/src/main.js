import Vue from 'vue'
import Vuex from 'vuex'
import VueTranslate from 'vue-translate-plugin';
import VueLocalStorage from 'vue-localstorage'

import App from './App'
import {locales} from './common/locales.js'

Vue.use(Vuex);
Vue.use(VueTranslate);
Vue.use(VueLocalStorage, {name: 'localstorage'})

Vue.locales(locales);

new Vue({
  el: '#app',
  router: require('./router').default,
  store: require('./store').default,
  template: '<App/>',
  components: { App }
})

Vue.directive('focus', {
  inserted: function (el) {
    el.focus()
  }
})