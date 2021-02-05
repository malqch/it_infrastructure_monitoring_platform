<template>
    <div>
        <div class="wrapper">
            <el-row class="serve_select">
                <el-form ref="form" label-width="100px">
                    <el-col :span="9">
                        <el-form-item label="达梦数据库">
                            <el-select
                                    v-model="dmDatabase"
                                    filterable
                                    remote
                                    reserve-keyword
                                    placeholder="请输入数据库名称或IP"
                                    :remote-method="queryDMDB"
                                    class="selectIp" @change="changeQueryHost">
                                <el-option
                                        v-for="(item) in dmData"
                                        :key=item.id
                                        :label="`${item.sid}/${item.ip_address}`"
                                        :value="`${item.sid}/${item.ip_address}`">
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
                <el-col :span="12">
                    <el-row>
                        <el-col :span="6">
                            <el-row class="dm_top_top">
                                <dl class="top_font_m20">
                                    <dt class="time">{{serveIp}}</dt>
                                    <dd>服务器IP</dd>
                                </dl>
                            </el-row>
                            <el-row class="dm_top_bot">
                                <dl class="top_font_m20">
                                    <dt class="serve_name">{{serveName}}</dt>
                                    <dd>数据库名称</dd>
                                </dl>
                            </el-row>
                        </el-col>
                        <el-col :span="11" class="dm_top_center">
                            <el-row class="dm_top_top">
                                <dl class="top_font_m20">
                                    <dt class="serve_name">{{serveVersion}}</dt>
                                    <dd>版本</dd>
                                </dl>
                            </el-row>
                            <el-row class="dm_top_bot">
                                <dl class="top_font_m20">
                                    <dt class="time">{{startTime}}</dt>
                                    <dd>开启时间</dd>
                                </dl>
                            </el-row>
                        </el-col>
                        <el-col :span="6">
                            <el-row class="dm_top_top dm_top_right">
                                <dl class="dm_top_font">
                                    <dt class="time">{{dmCpu}}</dt>
                                    <dd>cpu数量</dd>
                                </dl>
                            </el-row>
                            <el-row class="dm_top_bot dm_top_right">
                                <dl class="dm_top_font">
                                    <dt class="serve_name">{{Math.ceil(dmDiskTotal/1024/1024/1024)}} G</dt>
                                    <dd>磁盘容量</dd>
                                </dl>
                            </el-row>
                            <el-row class="dm_top_bot dm_top_right">
                                <dl class="dm_top_font">
                                    <dt class="serve_name">{{Math.ceil(phySize/1024/1024/1024)}} G</dt>
                                    <dd>内存容量</dd>
                                </dl>
                            </el-row>
                        </el-col>
                    </el-row>
                    <el-row class="serve_top_r_b mr10">
                        <div>
                            <p>cpu 15分钟平均负载</p>
                            <linegraph :id="'bargraphCpuFifteen'" :data="optionCpuFifteen" class="linegraph_dm"></linegraph>
                        </div>
                    </el-row>
                </el-col>
                <el-col :span="12">
                    <el-row class="serve_top_r_t">
                        <p>cpu 1分钟利用率</p>
                        <linegraph :id="'bargraphCpuOne'" :data="optionCpuOne" class="linegraph_dm"></linegraph>
                    </el-row>
                    <el-row class="serve_top_r_b">
                        <p>cpu 5分钟利用率</p>
                        <linegraph :id="'bargraphCpuFive'" :data="optionCpuFive" class="linegraph_dm"></linegraph>
                    </el-row>
                </el-col>
            </el-row>
            <el-row class="serve_center mlr10">
                <el-col :span="12">
                    <div class="serve_top_r_b mr10">
                        <p>每秒发送字节数</p>
                        <linegraph :id="'bargraphSendBytes'" :data="optionSendBytes" class="linegraph_dm"></linegraph>
                    </div>
                </el-col>
                <el-col :span="12" class="serve_top_r_b">
                    <p>每秒接收字节数</p>
                    <linegraph :id="'bargraphReciveBytes'" :data="optionReciveBytes" class="linegraph_dm"></linegraph>
                </el-col>
            </el-row>
            <el-row class="serve_center mlr10">
                <el-col :span="12">
                    <div class="serve_top_r_b mr10 dm_center_height">
                        <p>表空间</p>
                        <tableSpace :id="table_space_table" :data="table_space_table_data"></tableSpace>
                    </div>
                </el-col>
                <el-col :span="12">
                    <div class="serve_top_r_b dm_center_height">
                        <p>数据库对象</p>
                        <DMObjectInfo :id="object_info_table" :data="object_info_data"></DMObjectInfo>
                    </div>
                </el-col>
            </el-row>
            <el-row :span="24" class="serve_bottom mtb10">
                <div class="serve_bottom_left mlr10">
                    <p>缓冲池</p>
                    <bufferPool :id="buffer_pool_table" :data="buffer_pool_table_data"></bufferPool>
                </div>
            </el-row>
            <el-row :span="24" class="serve_bottom mtb10">
                <div class="serve_bottom_left mlr10">
                    <p>低效SQL</p>
                    <DMLongExecSql :id="long_exec_table" :data="long_exec_data"></DMLongExecSql>
                </div>
            </el-row>
        </div>
    </div>

</template>
<script>
    import linegraph from '../network_equipment/visualNetworkEchart/MinutesCpuUtilization.vue';
    import tableSpace from './dmEchart/TableSpace';
    import bufferPool from './dmEchart/BufferPool';
    import { timestampToTime } from '../../../util/formatData'
    import DMLongExecSql from "./dmEchart/DMLongExecSql";
    import DMObjectInfo from "./dmEchart/DMObjectInfo";

    export default {
        name: 'ViewServe',
        components: {
            // hitRateUtilization,
            tableSpace,
            bufferPool,
            DMLongExecSql,
            DMObjectInfo,
            linegraph
        },
        data(){
            return{
                serveName:'',
                serveIp:'10.10.10.130',
                serveVersion: '',
                startTime:'',

                table_space_table:'table_space_table',
                table_space_table_data:null,

                buffer_pool_table:'buffer_pool_table',
                buffer_pool_table_data:null,

                long_exec_table:'long_exec_table',
                long_exec_data:null,

                object_info_table:'object_info_table',
                object_info_data:null,
                optionCpuOne: {
                    title:'',
                    legendData:[],
                    xAxisData:[],
                    seriesData:[],
                    animation:true
                },
                optionCpuFive: {
                    title:'',
                    legendData:[],
                    xAxisData:[],
                    seriesData:[],
                    animation:true
                },
                optionCpuFifteen:{
                    title:'',
                    legendData:[],
                    xAxisData:[],
                    seriesData:[],
                    animation:true
                },
                optionReciveBytes: {
                    title:'',
                    legendData:[],
                    xAxisData:[],
                    seriesData:[],
                    animation:true
                },

                optionSendBytes:{
                    title:'',
                    legendData:[],
                    xAxisData:[],
                    seriesData:[],
                    animation:true
                },

                dmCpu:'',
                dmDiskTotal:'',
                phySize:'',
                monitorTime:'',
                dmData:null,
                dmDatabase:'',
                networkTime:[]
            }
        },
        computed: {
        },
        created() {
            this.networkTime=[this.Format(new Date()-12*60*60*1000), this.Format(new Date())];
            this.queryOneDM();
            this.timer=setInterval(()=>{this.changeQueryHost();},180000);
        },
        mounted() {
        },
        methods: {
            queryOneDM (){
                this.$http.get(`monitor/api/databases/?db_type=DM&current_page=1&pre_page=1&is_monitor=是`, {
                    headers: {'token':localStorage.getItem('token')}
                }).then((res) => {
                    const oneDMData = res.data;
                    const ip=oneDMData.data[0].ip_address;
                    const sid=oneDMData.data[0].sid;
                    this.dmDatabase=sid+'/'+ip;
                    this.optionData(ip,sid);
                    const curTime=Date.parse(this.networkTime[1])/1000;
                    const startTime=Date.parse(this.networkTime[0])/1000;
                    this.serveHistory(startTime,curTime,ip);
                }).catch( (error)=> {
                    this.$message.error(JSON.stringify(error.response.data));
                });
            },
            queryDMDB(query){
                if (query !== '') {
                    this.$http.get(`monitor/api/databases/search?db_type=DM&query=${query}&is_monitor=是`, {
                        headers: {'token':localStorage.getItem('token')}
                    }).then((res) => {
                        this.dmData = res.data;
                    }).catch( (error)=> {
                        this.$message.error(JSON.stringify(error.response.data));
                    });
                } else {
                    this.optionsNetworkIp = [];
                }
            },
            changeQueryHost(){
                const curTime=Date.parse(this.networkTime[1])/1000;
                const startTime=Date.parse(this.networkTime[0])/1000;
                const db_name=this.dmDatabase.split('/');
                const db_sid=db_name[0];
                const db_ip=db_name[1];
                this.optionData(db_ip,db_sid);
                this.serveHistory(startTime,curTime, db_ip);
            },
            optionData(db_ip,db_sid){
                this.$http.get(`monitor/api/databases/monitor/?db_name=DM_${db_ip}_${db_sid}`, {
                    headers:{
                        'token': this.token
                    }
                }).then((res)=>{
                    this.serveName=res.data.INSTALL_NAME;
                    this.serveIp=res.data.LOGIC_IP;
                    this.serveVersion=res.data.INSTANCE[0].SVR_VERSION
                    this.startTime=timestampToTime(res.data.INSTANCE[0].START_TIME/1000);

                    this.table_space_table_data=res.data.TABLE_SPACE;
                    this.buffer_pool_table_data=res.data.BUFFERPOOL;
                    this.long_exec_data = res.data.SQL_LONG_EXEC;
//                    this.object_info_data = res.data.OBJECT_INFO;
                    const info_data=res.data.OBJECT_INFO;
                    const info_xData=[];
                    const info_yData=[];
                    for(let item of info_data){
                        info_xData.push(item.OBJECT_TYPE);
                        info_yData.push(item.QUANTITY);
                    }
                    this.object_info_data={
                        xData:info_xData,
                        yData:info_yData
                    };

                    this.dmCpu=res.data.N_CPU;
                    this.dmDiskTotal=res.data.TOTAL_DISK_SIZE;
                    this.phySize=res.data.TOTAL_PHY_SIZE;
                }).catch( (error) => {
                    this.$message.error(JSON.stringify(error.response.data));
                });
            },
            serveHistory(startTime,curTime, ip) {
                this.$http.get(`monitor/api/databases/history/?start=` + startTime + `&end=` + curTime + `&m=sum:LOAD_ONE_AVERAGE{logicIp=${ip}}`, {
                    headers: {
                        'token': this.token
                    }
                }).then((res) => {
                    const lineTime = Object.keys(res.data);
                    const lineXtime = [];
                    for (let item in lineTime) {
                        lineXtime.push(this.Format(lineTime[item] * 1000));
                    }
                    const linevla = Object.values(res.data);
                    this.optionCpuOne.xAxisData=lineXtime;
                    this.optionCpuOne.seriesData=[{
                        name: "cpu 1分钟负载",
                        type: "line",
                        smooth: true,
                        symbol: 'circle',
                        symbolSize: 3,
                        lineStyle: {
                            normal: {
                                color:'#4bd459'
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
                                    offset: 0, color: 'rgba(75,212,89, 0.9)' // 0% 处的颜色
                                }, {
                                    offset: 0.8, color: 'rgba(75,212,89, 0)' // 100% 处的颜色
                                }],
                                global: false // 缺省为 false
                            },
                            shadowColor: 'rgba(0, 0, 0, 0.1)',
                            shadowBlur: 10
                        },
                        color: "#fff",
                        data:linevla
                    }];
                }).catch((error) => {
                    this.$message.error(JSON.stringify(error.response.data));
                });

                this.$http.get(`monitor/api/databases/history/?start=` + startTime + `&end=` + curTime + `&m=sum:LOAD_FIVE_AVERAGE{logicIp=${ip}}`, {
                    headers: {
                        'token': this.token
                    }
                }).then((res) => {
                    const lineTime = Object.keys(res.data);
                    const lineXtime = [];
                    for (let item in lineTime) {
                        lineXtime.push(this.Format(lineTime[item] * 1000));
                    }
                    const linevla = Object.values(res.data);
                    this.optionCpuFive.xAxisData=lineXtime;
                    this.optionCpuFive.seriesData=[{
                        name: "cpu 5分钟负载",
                        type: "line",
                        smooth: true,
                        symbol: 'circle',
                        symbolSize: 3,
                        lineStyle: {
                            normal: {
                                color:'#63d497'
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
                                    offset: 0, color: 'rgba(99,212,51, 0.9)' // 0% 处的颜色
                                }, {
                                    offset: 0.8, color: 'rgba(99,212,51, 0)' // 100% 处的颜色
                                }],
                                global: false // 缺省为 false
                            },
                            shadowColor: 'rgba(0, 0, 0, 0.1)',
                            shadowBlur: 10
                        },
                        color: "#fff",
                        data:linevla
                    }];
                }).catch((error) => {
                    this.$message.error(JSON.stringify(error.response.data));
                });

                this.$http.get(`monitor/api/databases/history/?start=` + startTime + `&end=` + curTime + `&m=sum:LOAD_FIFTEEN_AVERAGE{logicIp=${ip}}`, {
                    headers: {
                        'token': this.token
                    }
                }).then((res) => {
                    const lineTime = Object.keys(res.data);
                    const lineXtime = [];
                    for (let item in lineTime) {
                        lineXtime.push(this.Format(lineTime[item] * 1000));
                    }
                    const linevla = Object.values(res.data);
                    this.optionCpuFifteen.xAxisData=lineXtime;
                    this.optionCpuFifteen.seriesData=[{
                        name: "cpu 15分钟负载",
                        type: "line",
                        smooth: true,
                        symbol: 'circle',
                        symbolSize: 3,
                        lineStyle: {
                            normal: {
                                color:'#00d1b9'
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
                                    offset: 0, color: 'rgba(0,219,158, 0.9)' // 0% 处的颜色
                                }, {
                                    offset: 0.8, color: 'rgba(0,219,158, 0)' // 100% 处的颜色
                                }],
                                global: false // 缺省为 false
                            },
                            shadowColor: 'rgba(0, 0, 0, 0.1)',
                            shadowBlur: 10
                        },
                        color: "#fff",
                        data:linevla
                    }];
                }).catch((error) => {
                    this.$message.error(JSON.stringify(error.response.data));
                });

                this.$http.get(`monitor/api/databases/history/?start=` + startTime + `&end=` + curTime + `&m=sum:RECEIVE_BYTES_PER_SECOND{logicIp=${ip}}`, {
                    headers: {
                        'token': this.token
                    }
                }).then((res) => {
                    const lineTime = Object.keys(res.data);
                    const lineXtime = [];
                    for (let item in lineTime) {
                        lineXtime.push(this.Format(lineTime[item] * 1000));
                    }
                    const linevla = Object.values(res.data);
                    this.optionReciveBytes.xAxisData=lineXtime;
                    this.optionReciveBytes.seriesData=[{
                        name: "每秒接收字节数",
                        type: "line",
                        smooth: true,
                        symbol: 'circle',
                        symbolSize: 3,
                        lineStyle: {
                            normal: {
                                color:'#ccd14f'
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
                                    offset: 0, color: 'rgba(204,209,79, 0.9)' // 0% 处的颜色
                                }, {
                                    offset: 0.8, color: 'rgba(204,209,79, 0)' // 100% 处的颜色
                                }],
                                global: false // 缺省为 false
                            },
                            shadowColor: 'rgba(0, 0, 0, 0.1)',
                            shadowBlur: 10
                        },
                        color: "#fff",
                        data:linevla
                    }];
                }).catch((error) => {
                    this.$message.error(JSON.stringify(error.response.data));
                });

                this.$http.get(`monitor/api/databases/history/?start=` + startTime + `&end=` + curTime + `&m=sum:SEND_BYTES_PER_SECOND{logicIp=${ip}}`, {
                    headers: {
                        'token': this.token
                    }
                }).then((res) => {
                    const lineTime = Object.keys(res.data);
                    const lineXtime = [];
                    for (let item in lineTime) {
                        lineXtime.push(this.Format(lineTime[item] * 1000));
                    }
                    const linevla = Object.values(res.data);
                    this.optionSendBytes.xAxisData=lineXtime;
                    this.optionSendBytes.seriesData=[{
                        name: "每秒发送字节数",
                        type: "line",
                        smooth: true,
                        symbol: 'circle',
                        symbolSize: 3,
                        lineStyle: {
                            normal: {
                                color:'#d19968'
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
                                    offset: 0, color: 'rgba(209,153,104, 0.9)' // 0% 处的颜色
                                }, {
                                    offset: 0.8, color: 'rgba(209,153,104, 0)' // 100% 处的颜色
                                }],
                                global: false // 缺省为 false
                            },
                            shadowColor: 'rgba(0, 0, 0, 0.1)',
                            shadowBlur: 10
                        },
                        color: "#fff",
                        data:linevla
                    }];
                }).catch((error) => {
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
                return y + '-' + MM + '-' + d + ' ' + h + ':' + m ;
            }
        },
        beforeDestroy() {
            clearInterval(this.timer);
        }
    }
</script>
<style lang="scss" scoped>
    @import "../../../assets/css/fonts/font.css";
    @import "../../../assets/scss/echarts";
    .linegraph_dm{
        height: 170px;
    }
    .serve_top{
        margin: 13px 13px 0 13px;
    }
    .serve_top_r_t,.serve_top_r_b{
        height:200px;
        background:#24273e;
        border-radius: 10px;
        p{
            color:#03c2ec;
            font-size:12px;
            padding:10px 0 0 10px;
            font-weight: 600;
        }
    }
    .serve_top_r_b{
        margin-top:10px;
    }
    dl{

        .serve_name{
            font-size:18px;
        }
    }
    dl.dm_top_font{
        margin-top:10px;
        text-align: center;
        dd{
            margin-top:0;
        }
    }
    .dm_top_top,.dm_top_bot{
        height: 95px;
        border-radius: 10px;
        background:#24273e;
    }
    .dm_top_center{
        margin:0 7px;
    }
    .dm_top_bot{
        margin-top:10px;
    }
    .dm_top_right{
        height:60px;
    }

    .serve_bottom_left,.serve_bottom_right{
        height:330px;
        background:#24273e;
        border-radius: 10px;
    }
    .serve_center,.serve_bottom{
        p{
            color:#03c2ec;
            font-size:12px;
            padding:10px 0 0 10px;
            font-weight: 600;
        }
    }
    .dm_center_height{
        height:285px;
    }

    .top_font_m20{
        text-align: center;
        margin-top: 20px;
    }
</style>






