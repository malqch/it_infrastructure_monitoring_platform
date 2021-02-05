import Vue from 'vue';
import ElementUI from 'element-ui';
import axios from 'axios';
import 'element-ui/lib/theme-chalk/index.css'; // 默认主题
import './assets/css/icon.css';
import './application/asset/common/directives';
import 'babel-polyfill';
import AFTableColume from 'af-table-column';
import { hasBtnPermission } from './util/formatData';
import globalAPI from './util/globalAPI';
import {message} from './util/resetMessage';
import Echarts from 'echarts';
import htmlToPdf from '@/util/htmlToPdf';
import App from './App.vue';
import router from './router';

Vue.use(htmlToPdf);
Vue.config.productionTip = false;
Vue.prototype.$http = axios;
// axios.defaults.baseURL = '/api';

Vue.use(AFTableColume);

Vue.prototype.globalAPI = globalAPI;
Vue.prototype.hasPerm = hasBtnPermission;
Vue.prototype.$echarts=Echarts;

Vue.use(ElementUI, {
    size: 'small'
});
// Vue.use(message);
Vue.prototype.$message=message;
Vue.use(AFTableColume);


//使用钩子函数对路由进行权限跳转
router.beforeEach((to, from, next) => {
    document.title = `${to.meta.title} | 监控平台`;
    const role = localStorage.getItem('username');
    if (!role && to.path !== '/login') {
        next('/login');
    } else if (to.meta.permission) {
        // 如果是管理员权限则可进入，这里只是简单的模拟管理员权限而已
        role === 'admin' ? next() : next('/403');
    } else {
        // 简单的判断IE10及以下不进入富文本编辑器，该组件不兼容
        if (navigator.userAgent.indexOf('MSIE') > -1 && to.path === '/editor') {
            Vue.prototype.$alert('vue-quill-editor组件不兼容IE10及以下浏览器，请使用更高版本的浏览器查看', '浏览器不兼容通知', {
                confirmButtonText: '确定'
            });
        } else {
            next();
        }
    }
});

// 统一处理token失效问题
axios.interceptors.response.use(response => {
    return response;
},error => {
    if(error.response.status === 403){
        localStorage.clear();//删除用户信息
        Vue.prototype.$message.warning('登录超时，请重新登录！');
        router.replace({// 如果超时就处理 ，指定要跳转的页面
            path: '/login'
        });
    }else{
        return Promise.reject(error);
     }
});


new Vue({
    router,
    render: h => h(App)
}).$mount('#app');
