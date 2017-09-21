import Vue from 'vue'
import Router from 'vue-router'
import store from '@/store'

Vue.use(Router)

var router = new Router({
    mode:'history',
    routes: [{
        path: '/',
        component: require('@/components/Songslist.vue').default,
        name: 'root',
        auth: true
    },{
        path: '/song/display/:item_id(\\d+)',
        component: require('@/components/Song.vue').default,
        name: 'song_detail',
        auth: true
    },{
        path: '/song/compiled/pdf/:item_id(\\d+)',
        component: require('@/components/Songpdf.vue').default,
        name: 'song_pdf',
        auth: true
    },{
        path: '/song/add/',
        component: require('@/components/Songform.vue').default,
        name: 'song_new',
        auth: true
    },{
        path: '/song/edit/:item_id(\\d+)',
        component: require('@/components/Songeditform.vue').default,
        name: 'song_edit',
        auth: true
    },{
        path: '/song/force/latex/conversion/:item_id(\\d+)',
        component: require('@/components/Songtexform.vue').default,
        name: 'song_force_conversion',
        auth: true,
        props: { force_conversion: true }
    },{
        path: '/song/edit/latex/:item_id(\\d+)',
        component: require('@/components/Songtexform.vue').default,
        name: 'song_edit_latex',
        auth: true,
        props: { force_conversion: false },
    },{
        path: '/authors/',
        component: require('@/components/Authorlist.vue').default,
        name: 'authors_list',
        auth: true
    },{
        path: '/editors/',
        component: require('@/components/Editorlist.vue').default,
        name: 'editors_list',
        auth: true
    },{
        path: '/themes/',
        component: require('@/components/Themelist.vue').default,
        name: 'themes_list',
        auth: true
    },{
        path: '/chords/',
        component: require('@/components/Chordlist.vue').default,
        name: 'chords_list',
        auth: true
    },{
        path: '/logout/',
        component: require('@/components/Login.vue').default,
        name: 'logout',
        auth: true
    },{
        path: '/login/',
        component: require('@/components/Login.vue').default,
        name: 'login',
        auth: false
    }]
})


router.beforeEach(function (to, from, next) {
    if (!store.getters.has_jwt_token && to.name != "login") {
        // if route requires auth and user isn't authenticated
        console.log("MUST BE AUTHENTICATED")
        next('/login')
    } else {
        next()
    }
})

export default router