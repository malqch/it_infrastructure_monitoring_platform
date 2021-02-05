/**
 * Created by wangrj on 2020/6/11.
 */

const http8000='http://localhost:8000/';
const http8001='http://localhost:8001/';
const http8002='http://localhost:8002/';
const websocketUrl = 'ws://172.17.0.2:8003/';
const elkUrl = 'http://10.230.13.41:5601';
const nroUrl = 'http://10.230.13.41:9002';

export default {////将const创建的变量进行暴露，注意，暴露的必须是一个对象
    http8000,http8001,http8002,websocketUrl, elkUrl, nroUrl
}
