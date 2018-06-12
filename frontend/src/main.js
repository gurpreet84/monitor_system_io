import Vue from 'vue';
import iView from 'iview';
import VueRouter from 'vue-router';
import axios from 'axios'
import Routers from './router';
import Util from './libs/util';
import App from './app.vue';
import store from './store';
import VeLine from 'v-charts/lib/line';
import locale from 'iview/dist/locale/en-US'
import 'iview/dist/styles/iview.css';

Vue.use(VueRouter);
Vue.use(iView, { locale });
Vue.component(VeLine.name, VeLine);

Vue.prototype.$http = axios;


const RouterConfig = {
    mode: 'history',
    routes: Routers
};
const router = new VueRouter(RouterConfig);

router.beforeEach((to, from, next) => {
    iView.LoadingBar.start();
    Util.title(to.meta.title);
    if(window.localStorage.getItem('current_item')){
        store.commit('setItem', JSON.parse(window.localStorage.getItem('current_item')));
        next();
    }else{
        if(to.name == 'array_add'){
            next();
        }else{
            next({
                name: 'array_add'
            });
        }   
    }
    
});

router.afterEach((to, from, next) => {
    iView.LoadingBar.finish();
    window.scrollTo(0, 0);
});

new Vue({
    el: '#app',
    store: store,
    router: router,
    render: h => h(App)
});
