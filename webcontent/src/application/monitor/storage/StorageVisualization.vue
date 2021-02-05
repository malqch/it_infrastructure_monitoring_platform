<template>
    <div>
        <div class="wrapper">
            <el-row class="serve_select">
                <el-form ref="form" label-width="100px">
                    <el-col :span="9">
                        <el-form-item label="IP">
                            <el-select
                                    v-model="monitorIp"
                                    filterable
                                    remote
                                    reserve-keyword
                                    placeholder="请输入IP"
                                    :remote-method="queryHost"
                                    class="selectIp" @change="changeQueryHost">
                                <el-option
                                        v-for="(item) in IPData"
                                        :key=item.id
                                        :label="`${item.hostname}/${item.manage_ip}`"
                                        :value="`${item.hostname}/${item.manage_ip}`">
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
                <el-col :span="6">
                    <div class="serve_top_sub">
                        <dl class="top_font_10">
                            <dt class="serve_name">{{IP}}</dt>
                            <dd>IP</dd>
                        </dl>
                    </div>
                    <div class="serve_top_sub mtb10">
                        <dl class="top_font_10">
                            <dt class="time">{{MONITOR_TYPE}}</dt>
                            <dd>MONITOR_TYPE</dd>
                        </dl>
                    </div>
                    <div class="serve_top_sub">
                        <dl class="top_font_10">
                            <dt class="time">{{INSTALL_NAME}}</dt>
                            <dd>INSTALL_NAME</dd>
                        </dl>
                    </div>
                </el-col>
                <el-col :span="18" class="serve_center">
                    <div class="serve_center_left">
                        <p>各存储指标项</p>
                        <monitorEcharts :id="'monitor'" :data="monitorData"></monitorEcharts>
                    </div>
                </el-col>
            </el-row>
            <el-row class="serve_bottom">
                <el-row :span="24" class="network_cpu">
                    <p>某一时间段内各指标项历史值</p>
                    <el-col :span="8" v-for="(item,index) in optionsData" :key="index" class="chart-item-area">
                        <historyMointor
                                :data="item"
                                :id='"charts" +index'
                                :index="index"
                                class="cpuHeight"
                        ></historyMointor>
                    </el-col>
                </el-row>
            </el-row>
        </div>
    </div>

</template>
<script>
import monitorEcharts from '../network_equipment/visualNetworkEchart/monitorBar.vue';
import historyMointor from '../network_equipment/visualNetworkEchart/MinutesCpuUtilization.vue';

export default {
    name: 'ViewServe',
    components: {
        monitorEcharts,
        historyMointor
    },
    data(){
        return{
            timer:null,
            networkTime:[],
            monitorIp:'',
            INSTALL_NAME:'',
            MONITOR_TYPE:'',
            IP:'',
            IPData:[],
            monitorData:{
                xAxisData:[],
                seriesData:[]
            },
            optionsData:[]
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
        queryOneServe(){
            this.$http.get(`asset/api/storage/?current_page=1&pre_page=1`, {
                headers:
                    {
                        'token':localStorage.getItem('token')
                    }
            }).then((res) => {
                const ip=res.data.data[0].manage_ip;
                const hostname=res.data.data[0].hostname;
                this.monitorIp=hostname+'/'+ip;
                const start=this.networkTime[0].replace(/-/g,'/').replace(/\s/g,'-');
                const end=this.networkTime[1].replace(/-/g,'/').replace(/\s/g,'-');
                this.optionData(ip,start,end);
            }).catch( (error)=> {
                this.$message.error(JSON.stringify(error.response.data));
            });
        },
        queryHost(query){
            if (query !== '') {
                 this.$http.get(`asset/api/storage/storage/?query=${query}`, {
                    headers:
                 {
                     'token':localStorage.getItem('token')
                 }
                 }).then((res) => {
                     this.IPData = res.data;
                 }).catch( (error)=> {
                    this.$message.error(JSON.stringify(error.response.data));
                 });
            } else {
                this.optionsNetworkIp = [];
            }
        },
        changeQueryHost(){
            const ip=this.monitorIp.split('/');
            const monitor_ip=ip[1];
            const start=this.Format(this.networkTime[0]).replace(/-/g,'/').replace(/\s/g,'-');
            const end=this.Format(this.networkTime[1]).replace(/-/g,'/').replace(/\s/g,'-');
            this.optionsData=[];
            this.optionData(monitor_ip,start,end);
        },
        optionData(ip,start,end){
            this.$http.get(`monitor/api/storageitem/monitor/?storage_name=STORAGE_${ip}_3`, {
                headers:{
                    'token': this.token
                }
            }).then((res)=>{
                if(res.data.INSTALL_NAME==undefined){
                    this.$message.warning('未查询到数据');
                    return false;
                }
                this.INSTALL_NAME=res.data.INSTALL_NAME;
                this.MONITOR_TYPE=res.data.MONITOR_TYPE;
                this.IP=res.data.LOGIC_IP;
                const monitor_xAxis=res.data.monitor.map( item =>{return item.key});
                const monitor_series=res.data.monitor.map( item =>{return item.value});
                this.monitorData.xAxisData=monitor_xAxis;
                this.monitorData.seriesData=[{
                    type: 'bar',
                    data: monitor_series,
                    barWidth: '20px',
                    itemStyle: {
                        normal: {
                            color: new this.$echarts.graphic.LinearGradient(0, 0, 0, 1, [{
                                offset: 0,
                                color: 'rgba(0,244,255,1)' // 0% 处的颜色
                            }, {
                                offset: 1,
                                color: 'rgba(0,77,167,1)' // 100% 处的颜色
                            }], false),
                            barBorderRadius: [30, 30, 30, 30],
                            shadowColor: 'rgba(0,160,221,1)',
                            shadowBlur: 4,
                        }
                    }
                }];
                for(let item of monitor_xAxis){
                    let chartListObj={};
                    chartListObj.title='指标项'+item;
                    chartListObj.legendData=['流量'];
                    this.$http.get(`/monitor/api/storageitem/history/?start=${start}&end=${end}&m=sum:${item}`, {
                        headers:{
                            'token': this.token
                        }
                    }).then( (res)=>{
                        const chartsData=res.data;
                        const chartsTime=Object.keys(chartsData);
                        const chartsVal=Object.values(chartsData);
                        let xAxis=chartsTime.map( item =>{
                            return this.Format(item*1000);
                        });
                        chartListObj.xAxisData=xAxis;
                        chartListObj.seriesData=[
                            {
                                name: "值",
                                type: "line",
                                smooth: true,
                                symbol: 'circle',
                                symbolSize: 3,
                                lineStyle: {
                                    normal: {
                                        color:'#9e8cff'
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
                                            offset: 0, color: 'rgba(158,140,255, 0.8)' // 0% 处的颜色
                                        }, {
                                            offset: 0.8, color: 'rgba(158,140,255, 0)' // 100% 处的颜色
                                        }],
                                        global: false // 缺省为 false
                                    },
                                    shadowColor: 'rgba(0, 0, 0, 0.1)',
                                    shadowBlur: 10
                                },
                                itemStyle: {
                                    normal: {
                                        color: '#9e8cff',
                                        borderColor: '#9e8cff'
                                    }
                                },
                                data:chartsVal
                            }
                        ]
                        this.optionsData.push(chartListObj);
                    }).catch( (error) => {
                        this.$message.error(JSON.stringify(error.response.data));
                    });
                }
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
            let s = date.getSeconds();
            s = s < 10 ? ('0' + s) : s;
            return y + '-' + MM + '-' + d + ' ' + h + ':' + m +':'+s;

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
    .cpuHeight{
        height:220px;
        padding:6px 0;
    }
    .serve_top{
        border-radius: 10px;
        margin:13px 13px;
    }
    .serve_top_sub_left,.serve_top_sub{
        border-radius: 10px;
        background:#24273e;
    }
    .serve_top_sub_139{
        height:139px!important;
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






