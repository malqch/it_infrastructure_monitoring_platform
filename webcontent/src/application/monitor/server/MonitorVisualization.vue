<template>
    <div>
        <div class="wrapper">
            <el-row class="serve_select">
                <el-form ref="form" label-width="100px">
                    <el-col :span="9">
                        <el-form-item label="主机名称">
                            <el-select
                                    v-model="serveHost"
                                    filterable
                                    remote
                                    reserve-keyword
                                    placeholder="请输入服务器名称或IP"
                                    :remote-method="queryHost"
                                    class="selectIp" @change="changeQueryHost">
                                <el-option
                                        v-for="(item) in hostData"
                                        :key=item.id
                                        :label="`${item.hostname}/${item.ip}`"
                                        :value="`${item.hostname}/${item.ip}`">
                                </el-option>
                            </el-select>
                        </el-form-item>
                    </el-col>
                    <el-col :span="15">
                        <el-form-item label="起止日期">
                            <el-date-picker
                                    v-model="networkTime"
                                    type="datetimerange"
                                    range-separator="至"
                                    start-placeholder="开始日期"
                                    end-placeholder="结束日期"
                                    class="mt16"
                                    @change="changeQueryHost">
                            </el-date-picker>
                        </el-form-item>
                    </el-col>
                </el-form>
            </el-row>
            <el-row class="serve_top">
                <el-col :span="8" class="serve_top_sub_left">
                    <div type="flex" class="row-bg" justify="space-around">
                        <el-col :span="7">
                            <cpuUtilization :id="cpuUse" :data="CpuData"></cpuUtilization>
                        </el-col>
                        <el-col :span="7">
                            <memUtilization :id="memUse" :data="memData"></memUtilization>
                        </el-col>
                        <el-col :span="7">
                            <diskUtilization :id="diskUse" :data="diskData"></diskUtilization>
                        </el-col>
                    </div>
                </el-col>
                <el-col :span="16">
                    <el-row>
                        <el-col :span="10">
                            <div class="serve_top_sub serve_top_sub_le">
                                <dl class="top_font_10">
                                    <dt class="serve_name">{{serveName}}</dt>
                                    <dd>服务器名称</dd>
                                </dl>
                            </div>
                        </el-col>
                        <el-col :span="5">
                            <div class="serve_top_sub mlr10">
                                <dl class="top_font_10">
                                    <dt class="time">{{serveIp}}</dt>
                                    <dd>服务器IP</dd>
                                </dl>
                            </div>
                        </el-col>
                        <el-col :span="9">
                            <div class="serve_top_sub">
                                <dl class="top_font_10">
                                    <dt class="time">{{startTime}}</dt>
                                    <dd>开启时间</dd>
                                </dl>
                            </div>
                        </el-col>
                    </el-row>
                    <el-row>
                        <el-col :span="4">
                            <div class="serve_top_right serve_top_m">
                                <dl class="top_font_10">
                                    <dt class="time">{{cpuCount}}</dt>
                                    <dd>cpu数量</dd>
                                </dl>
                            </div>
                        </el-col>
                        <el-col :span="5">
                            <div class="serve_top_right serve_top_mt">
                                <dl class="top_font_10">
                                    <dt class="time">{{parseInt(Math.round(totalMem/1024/1024/1024))}}</dt>
                                    <dd>内存容量(G)</dd>
                                </dl>
                            </div>
                        </el-col>
                        <el-col :span="5">
                            <div  class="serve_top_right">
                                <dl class="top_font_10">
                                    <dt class="time">{{totalDisk}}</dt>
                                    <dd>磁盘容量(G)</dd>
                                </dl>
                            </div>
                        </el-col>
                        <el-col :span="5">
                            <div class="serve_top_right serve_top_mt">
                                <dl class="top_font_10">
                                    <dt class="time">{{process}}</dt>
                                    <dd>进程数量</dd>
                                </dl>
                            </div>
                        </el-col>
                        <el-col :span="5">
                            <div class="serve_top_right">
                                <dl class="top_font_10">
                                    <dt class="serve_name">{{osName}}</dt>
                                    <dd>操作系统</dd>
                                </dl>
                            </div>
                        </el-col>
                    </el-row>
                </el-col>
            </el-row>
            <el-row class="serve_center serve_center_m">
                <el-col :span="11" class="serve_center_left">
                    <p>cpu历史利用率</p>
                    <linegraph :id="'bargraph'" :data="optionCpu" class="linegraph_network"></linegraph>
                </el-col>
                <el-col :span="12" class="serve_center_right">
                    <p>cpu IOwait</p>
                    <linegraph :id="'bargraphCpuSysIoWait'" :data="optionCpuIoWait" class="linegraph_network"></linegraph>
                </el-col>
            </el-row>
            <el-row class="serve_center serve_center_m">
                <el-col :span="11" class="serve_center_left">
                    <p>cpu用户使用率</p>
                    <linegraph :id="'bargraphCpuUser'" :data="optionCpuUser" class="linegraph_network"></linegraph>
                </el-col>
                <el-col :span="12" class="serve_center_right">
                    <p>cpu系统使用率</p>
                    <linegraph :id="'bargraphCpuSys'" :data="optionCpuSys" class="linegraph_network"></linegraph>
                </el-col>
            </el-row>
            <el-row class="serve_center serve_center_m">
                <el-col :span="11" class="serve_center_left">
                    <p>内存历史利用率</p>
                    <linegraph :id="'bargraphMem'" :data="optionMem" class="linegraph_network"></linegraph>
                </el-col>
                <el-col :span="12" class="serve_center_right">
                    <p>swap使用率</p>
                    <linegraph :id="'bargraphSwapPercent'" :data="optionSwapPercent" class="linegraph_network"></linegraph>
                </el-col>
            </el-row>
            <el-row class="serve_bottom">
                <p>磁盘详细信息列表</p>
                <diskMessageList :id="diskList" :data="diskListData"></diskMessageList>
            </el-row>
            <el-row class="serve_bottom">
                <p>网络接口信息列表</p>
                <networkPortList :id="networkList" :data="networkListData"></networkPortList>
            </el-row>
        </div>
    </div>

</template>
<script>
    import linegraph from '../network_equipment/visualNetworkEchart/MinutesCpuUtilization.vue';
    import cpuUtilization from './visualServeEchart/cpuUtilization';
    import memUtilization from './visualServeEchart/memUtilization';
    import diskUtilization from './visualServeEchart/diskUtilization';
    import diskMessageList from './visualServeEchart/diskList.vue';
    import networkPortList from './visualServeEchart/networkList.vue';

export default {
    name: 'ViewServe',
    components: {
        cpuUtilization,
        memUtilization,
        diskUtilization,
        linegraph,
        diskMessageList,
        networkPortList
    },
    data(){
        return{
            cpuUse:'cpuUse',
            CpuData:0,

            memUse:'memUse',
            memData:0,

            diskUse:'diskUse',
            diskData:0,

            optionCpu:{
                title:'',
                legendData:[],
                xAxisData:[],
                seriesData:[],
                animation:true
            },

            optionMem:{
                title:'',
                legendData:[],
                xAxisData:[],
                seriesData:[],
                animation:true
            },

            optionCpuUser:{
                title:'',
                legendData:[],
                xAxisData:[],
                seriesData:[],
                animation:true
            },

            optionCpuSys:{
                title:'',
                legendData:[],
                xAxisData:[],
                seriesData:[],
                animation:true
            },
            optionSwapPercent: {
                title:'',
                legendData:[],
                xAxisData:[],
                seriesData:[],
                animation:true
            },

            optionCpuIoWait: {
                title:'',
                legendData:[],
                xAxisData:[],
                seriesData:[],
                animation:true
            },

            serveName:'',

            networkList:'networkList',
            networkListData:null,

            serveIp:'10.10.10.130',
            startTime:'',

            diskList:'diskList',
            diskListData:null,
            timer:null,

            cpuCount:null,
            totalDisk:0,
            osName:null,
            process:null,
            totalMem:null,
            serveHost:'',
            hostData:null,
            networkTime:[]
        }
    },
    computed: {
    },
    created() {
        this.networkTime=[this.Format(new Date()-12*60*60*1000), this.Format(new Date())];
        this.queryOneServe();
        this.timer=setInterval(()=>{
            this.changeQueryHost();
        },180000);
    },
    mounted() {
    },
    methods: {
        queryOneServe (){
            this.$http.get(`asset/api/virtual_server?current_page=1&pre_page=1&is_monitor=是`, {
                headers:
                    {
                        'token':localStorage.getItem('token')
                    }
            }).then((res) => {
                const oneHostData = res.data;
                const ip=oneHostData.data[0].virtual_ip;
                const hostname=oneHostData.data[0].hostname;
                this.serveHost=hostname+'/'+ip;
                this.optionData(ip,hostname);
                const curTime=Date.parse(this.networkTime[1])/1000;
                const startTime=Date.parse(this.networkTime[0])/1000;
                this.serveHistory(startTime,curTime,ip);
            }).catch( (error)=> {
                this.$message.error(JSON.stringify(error.response.data));
            });
        },
        queryHost(query){
            if (query !== '') {
                 this.$http.get(`asset/api/device/device_virtualserver?query=${query}&is_monitor=是`, {
                    headers:
                 {
                     'token':localStorage.getItem('token')
                 }
                 }).then((res) => {
                     this.hostData = res.data;
                 }).catch( (error)=> {
                    this.$message.error(JSON.stringify(error.response.data));
                 });
            } else {
                this.optionsNetworkIp = [];
            }
        },
        changeQueryHost(){
            const serve_name=this.serveHost.split('/');
            const serve_host=serve_name[0];
            const serve_ip=serve_name[1];
            this.optionData(serve_ip,serve_host);
            const curTime=Date.parse(this.networkTime[1])/1000;
            const startTime=Date.parse(this.networkTime[0])/1000;
            this.serveHistory(startTime,curTime,serve_ip);
        },
        optionData(serve_ip,serve_host){
            this.$http.get(`monitor/api/server_monitor/monitor/?server_name=SERVER_${serve_ip}_${serve_host}`, {
                headers:{
                    'token': this.token
                }
            }).then((res)=>{
                if(res.data.INSTALL_NAME==undefined ){
                    this.$message.warning('未查询到数据！');
                    this.serveName='';
                    this.serveIp='';
                    this.startTime='';
                    this.CpuData=0;
                    this.memData=0;

                    this.diskData=0;
                    this.diskListData=null;
                    this.networkListData=null;
                    this.cpuCount='';
                    this.totalDisk='';
                    this.osName='';
                    this.process='';
                    this.totalMem='';
                    return false;
                }
                this.serveName=res.data.INSTALL_NAME;
                this.serveIp=res.data.LOGIC_IP;
                this.startTime=res.data.START_TIME;
                this.CpuData=(Math.round(res.data.CPU_PERCENT))/100;
                this.memData=(Math.round(res.data.MEM_PERCENT))/100;
                this.diskData=Math.round(res.data.DISK_RATE)/100;
                this.diskListData=res.data.DISK_DETAIL;
                this.networkListData=res.data.NET_IO_COUNTERS;
                this.cpuCount=res.data.CPU_COUNT;
                const total_disk=res.data.TOTAL_DISK.split('GB');
                this.totalDisk=parseInt(Math.round(total_disk[0]));
                this.osName=res.data.OS_NAME;
                this.process=res.data.PROCESS;
                this.totalMem=res.data.TOTAL_MEM;
            }).catch( (error) => {
                this.$message.error(JSON.stringify(error.response.data));
            });
        },
        serveHistory(startTime,curTime,ip){
            this.$http.get(`monitor/api/server_monitor/history/?start=`+startTime+`&end=`+curTime+`&m=sum:CPU_PERCENT{logicIp=${ip}}`, {
                headers:{
                    'token': this.token
                }
            }).then((res)=>{
                if(res.detail=="未查询到数据！"){
                    return false;
                }
                const lineTime=Object.keys(res.data);
                const lineXtime=[];
                for(let item in lineTime){
                    lineXtime.push(this.Format(lineTime[item]*1000));
                }
                const linevla=Object.values(res.data);
                this.optionCpu.xAxisData=lineXtime;
                this.optionCpu.seriesData=[{
                    name: "cpu",
                    type: "line",
                    smooth: true,
                    symbol: 'circle',
                    symbolSize: 3,
                    lineStyle: {
                        normal: {
                            color:'#d1b25b'
                        },
                    },
                    areaStyle:{
                        color: {
                            type: 'linear',
                            x: 0,
                            y: 0,
                            x2: 0,
                            y2: 1,
                            colorStops: [{
                                offset: 0, color: 'rgba(209,178,91, 0.9)' // 0% 处的颜色
                            }, {
                                offset: 0.8, color: 'rgba(209,178,91, 0)' // 100% 处的颜色
                            }],
                            global: false // 缺省为 false
                        },
                        shadowColor: 'rgba(0, 0, 0, 0.1)',
                        shadowBlur: 10
                    },
                    color: "#fff",
                    data:linevla
                }];
            }).catch( (error) => {
                this.$message.error(JSON.stringify(error.response.data));
            });
            this.$http.get(`monitor/api/server_monitor/history/?start=`+startTime+`&end=`+curTime+`&m=sum:MEM_PERCENT{logicIp=${ip}}`, {
                headers:{
                    'token': this.token
                }
            }).then((res)=>{
                if(res.detail=="未查询到数据！"){
                    return false;
                }
                const lineTime=Object.keys(res.data);
                const lineXtime=[];
                for(let item in lineTime){
                    lineXtime.push(this.Format(lineTime[item]*1000));
                }
                const linevla=Object.values(res.data);
                this.optionMem.xAxisData=lineXtime;
                this.optionMem.seriesData=[{
                    name: "内存",
                    type: "line",
                    smooth: true,
                    symbol: 'circle',
                    symbolSize: 3,
                    lineStyle: {
                        normal: {
//                                color: "#b996f8",
                            color:'#da6240'
                        },
                    },
                    areaStyle:{
                        color: {
                            type: 'linear',
                            x: 0,
                            y: 0,
                            x2: 0,
                            y2: 1,
                            colorStops: [{
                                offset: 0, color: 'rgba(218,98,64, 0.9)' // 0% 处的颜色
                            }, {
                                offset: 0.8, color: 'rgba(218,98,64, 0)' // 100% 处的颜色
                            }],
                            global: false // 缺省为 false
                        },
                        shadowColor: 'rgba(0, 0, 0, 0.1)',
                        shadowBlur: 10
                    },
                    color: "#fff",
                    data: linevla
                }];
            }).catch( (error) => {
                this.$message.error(JSON.stringify(error.response.data));
            });

            this.$http.get(`monitor/api/server_monitor/history/?start=`+startTime+`&end=`+curTime+`&m=sum:CPU_USER{logicIp=${ip}}`, {
                headers:{
                    'token': this.token
                }
            }).then((res)=>{
                if(res.detail=="未查询到数据！"){
                    return false;
                }
                const lineTime=Object.keys(res.data);
                const lineXtime=[];
                for(let item in lineTime){
                    lineXtime.push(this.Format(lineTime[item]*1000));
                }

                const linevla=Object.values(res.data);
                this.optionCpuUser.xAxisData=lineXtime;
                this.optionCpuUser.seriesData=[{
                    name: "cpu用户占用百分比",
                    type: "line",
                    smooth: true,
                    symbol: 'circle',
                    symbolSize: 3,
                    lineStyle: {
                        normal: {
                            color:'#9fda51'
                        },
                    },
                    areaStyle:{
                        color: {
                            type: 'linear',
                            x: 0,
                            y: 0,
                            x2: 0,
                            y2: 1,
                            colorStops: [{
                                offset: 0, color: 'rgba(159,218,81, 0.9)' // 0% 处的颜色
                            }, {
                                offset: 0.8, color: 'rgba(159,218,81, 0)' // 100% 处的颜色
                            }],
                            global: false // 缺省为 false
                        },
                        shadowColor: 'rgba(0, 0, 0, 0.1)',
                        shadowBlur: 10
                    },
                    color: "#fff",
                    data:linevla
                }];
            }).catch( (error) => {
                this.$message.error(JSON.stringify(error.response.data));
            });

            this.$http.get(`monitor/api/server_monitor/history/?start=`+startTime+`&end=`+curTime+`&m=sum:CPU_SYSTEM{logicIp=${ip}}`, {
                headers:{
                    'token': this.token
                }
            }).then((res)=>{
                if(res.detail=="未查询到数据！"){
                    return false;
                }
                const lineTime=Object.keys(res.data);
                const lineXtime=[];
                for(let item in lineTime){
                    lineXtime.push(this.Format(lineTime[item]*1000));
                }
                const linevla=Object.values(res.data);
                this.optionCpuSys.xAxisData=lineXtime;
                this.optionCpuSys.seriesData=[{
                    name: "cpu系统使用率",
                    type: "line",
                    smooth: true,
                    symbol: 'circle',
                    symbolSize: 3,
                    lineStyle: {
                        normal: {
//                                color: "#b996f8",
                            color:'#7c94da'
                        },
                    },
                    areaStyle:{
                        color: {
                            type: 'linear',
                            x: 0,
                            y: 0,
                            x2: 0,
                            y2: 1,
                            colorStops: [{
                                offset: 0, color: 'rgba(124,148,218, 0.9)' // 0% 处的颜色
                            }, {
                                offset: 0.8, color: 'rgba(124,148,218, 0)' // 100% 处的颜色
                            }],
                            global: false // 缺省为 false
                        },
                        shadowColor: 'rgba(0, 0, 0, 0.1)',
                        shadowBlur: 10
                    },
                    color: "#fff",
                    data: linevla
                }];
            }).catch( (error) => {
                this.$message.error(JSON.stringify(error.response.data));
            });

            this.$http.get(`monitor/api/server_monitor/history/?start=`+startTime+`&end=`+curTime+`&m=sum:SWAP_PERCENT{logicIp=${ip}}`, {
                headers:{
                    'token': this.token
                }
            }).then((res)=>{
                if(res.detail=="未查询到数据！"){
                    return false;
                }
                const lineTime=Object.keys(res.data);
                const lineXtime=[];
                for(let item in lineTime){
                    lineXtime.push(this.Format(lineTime[item]*1000));
                }
                const linevla=Object.values(res.data);
                this.optionSwapPercent.xAxisData=lineXtime;
                this.optionSwapPercent.seriesData=[{
                    name: "Swap使用百分比",
                    type: "line",
                    smooth: true,
                    symbol: 'circle',
                    symbolSize: 3,
                    lineStyle: {
                        normal: {
//                                color: "#b996f8",
                            color:'#da3914'
                        },
                    },
                    areaStyle:{
                        color: {
                            type: 'linear',
                            x: 0,
                            y: 0,
                            x2: 0,
                            y2: 1,
                            colorStops: [{
                                offset: 0, color: 'rgba(218,57,20, 0.9)' // 0% 处的颜色
                            }, {
                                offset: 0.8, color: 'rgba(218,57,20, 0)' // 100% 处的颜色
                            }],
                            global: false // 缺省为 false
                        },
                        shadowColor: 'rgba(0, 0, 0, 0.1)',
                        shadowBlur: 10
                    },
                    color: "#fff",
                    data: linevla
                }];
            }).catch( (error) => {
                this.$message.error(JSON.stringify(error.response.data));
            });

            this.$http.get(`monitor/api/server_monitor/history/?start=`+startTime+`&end=`+curTime+`&m=sum:IOWAIT{logicIp=${ip}}`, {
                headers:{
                    'token': this.token
                }
            }).then((res)=>{
                if(res.detail=="未查询到数据！"){
                    return false;
                }
                const lineTime=Object.keys(res.data);
                const lineXtime=[];
                for(let item in lineTime){
                    lineXtime.push(this.Format(lineTime[item]*1000));
                }
                const linevla=Object.values(res.data);
                this.optionCpuIoWait.xAxisData=lineXtime;
                this.optionCpuIoWait.seriesData=[{
                    name: "cpu iowait",
                    type: "line",
                    smooth: true,
                    symbol: 'circle',
                    symbolSize: 3,
                    lineStyle: {
                        normal: {
                            color:'#a96ada'
                        },
                    },
                    areaStyle:{
                        color: {
                            type: 'linear',
                            x: 0,
                            y: 0,
                            x2: 0,
                            y2: 1,
                            colorStops: [{
                                offset: 0, color: 'rgba(169,106,218, 0.9)' // 0% 处的颜色
                            }, {
                                offset: 0.8, color: 'rgba(169,106,218, 0)' // 100% 处的颜色
                            }],
                            global: false // 缺省为 false
                        },
                        shadowColor: 'rgba(0, 0, 0, 0.1)',
                        shadowBlur: 10
                    },
                    color: "#fff",
                    data: linevla
                }];
            }).catch( (error) => {
                this.$message.error(JSON.stringify(error.response.data));
            });
        },
        Format(value){
            let date = new Date(value);
            let y = date.getFullYear();
            let MM = date.getMonth() + 1;
            MM = MM < 10 ? ('0' + MM) : MM;
            let d = date.getDate();
            d = d < 10 ? ('0' + d) : d;
            let h = date.getHours();
            h = h < 10 ? ('0' + h) : h;
            let m = date.getMinutes();
            m = m < 10 ? ('0' + m) : m;
//            let s = date.getSeconds();
//            s = s < 10 ? ('0' + s) : s;
            return y + '-' + MM + '-' + d + ' ' + h + ':' + m ;

        }
    },
    beforeDestroy() {
        clearInterval(this.timer);
        this.timer = null;
    }
}


</script>
<style lang="scss" scoped>
    @import "../../../assets/css/fonts/font.css";
    @import "../../../assets/scss/echarts";
    .linegraph_network{
        height: 170px;
    }
    .serve_top{
        border-radius: 10px;
        margin:13px 13px;
        height:145px;
    }
    .serve_top_sub_left,.serve_top_sub{
        border-radius: 10px;
        background:#24273e;
    }
    .serve_top_sub_le{
        margin-left:12px;
    }
    .serve_top_sub{
        height: 65px;
    }

    .serve_bottom{
        background:#24273e;
        border-radius: 10px;
        margin:13px 13px;
    }
    .serve_center_left,.serve_center_right{
        background:#24273e;
        border-radius: 10px;
    }
    .serve_center_left{
        margin:0 15px 0 15px;
    }
    .serve_top_right{
        height: 70px;
        background: #24273e;
        border-radius: 8px;
        margin-top: 10px;
    }
    .serve_top_m{
        margin-left:13px;
    }
    .serve_top_mt{
        margin:10px 12px;
    }
    dl{
        dd{
            margin-top: 3px;
        }
    }
    .serve_bottom_left,.serve_bottom_right{
        height:50px;
        background:#24273e;
        border-radius: 10px;
    }
    .serve_bottom_left{
        margin:0 13px 0 13px;
    }
    .serve_center,.serve_bottom{
        p{
            color:#03c2ec;
            font-size:12px;
            padding:10px 0 0 10px;
            font-weight: 600;
        }
    }
    .serve_center_m{
        margin-top:10px;
    }
</style>






