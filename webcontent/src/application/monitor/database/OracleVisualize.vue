<template>
    <div>
        <div class="wrapper">
            <el-row class="serve_select">
                <el-form ref="form" label-width="100px">
                    <el-col :span="9">
                        <el-col>
                            <el-form-item label="oracle">
                                <el-select
                                        v-model="oracleDatabase"
                                        filterable
                                        remote
                                        reserve-keyword
                                        placeholder="请输入数据库名称或IP"
                                        :remote-method="queryOracleDB"
                                        class="selectIp" @change="changeQueryHost">
                                    <el-option
                                            v-for="(item) in oracleData"
                                            :key=item.id
                                            :label="`${item.sid}/${item.ip_address}`"
                                            :value="`${item.sid}/${item.ip_address}`">
                                    </el-option>
                                </el-select>
                            </el-form-item>
                        </el-col>
                    </el-col>
                    <el-col :span="15">
                        <el-form-item label="起止日期">
                            <el-date-picker
                                    v-model="monitorTime"
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
            <el-row class="serve_top m10">
                <el-col :span="9">
                    <div type="flex" class="row-bg serve_top_left" justify="space-around">
                        <el-col :span="8">
                            <OracleHitRatio :id="hit_ratio_use" :data="hit_ratio_data"></OracleHitRatio>
                        </el-col>
                        <el-col :span="8">
                            <OracleSgaRate :id="sga_rate_use" :data="sga_rate_data"></OracleSgaRate>
                        </el-col>
                        <el-col :span="8">
                            <OraclePgaRate :id="pga_rate_use" :data="pga_rate_data"></OraclePgaRate>
                        </el-col>
                    </div>
                </el-col>
                <el-col :span="15">
                    <el-col :span="5">
                        <div class="serve_top_char ml10">
                            <dl class="top_font">
                                <dt class="time">{{serveIp}}</dt>
                                <dd>服务器IP</dd>
                            </dl>
                        </div>
                    </el-col>
                    <el-col :span="5">
                        <div class="serve_top_char mlr10">
                            <dl class="top_font">
                                <dt class="time">{{version}}</dt>
                                <dd>版本</dd>
                            </dl>
                        </div>
                    </el-col>
                    <el-col :span="5">
                        <div class="serve_top_char">
                            <dl class="top_font">
                                <dt class="serve_name">{{instance_name}}</dt>
                                <dd>实例名称</dd>
                            </dl>
                        </div>
                    </el-col>
                    <el-col :span="9">
                        <div class="serve_top_char ml10">
                            <dl class="top_font">
                                <dt class="time">{{star_time}}</dt>
                                <dd>启动时间</dd>
                            </dl>
                        </div>
                    </el-col>
                </el-col>
            </el-row>
            <el-row class="serve_top_80 mlr10 mb10">
                <el-col :span="24">
                    <el-col :span="5">
                        <div class="serve_top_char_80 mr10">
                            <dl class="top_font_10">
                                <dt class="time">{{active_session_count}}</dt>
                                <dd>激活session</dd>
                            </dl>
                        </div>
                    </el-col>
                    <el-col :span="5">
                        <div class="serve_top_char_80 mr10">
                            <dl class="top_font_10">
                                <dt class="time">{{inactive_session_count}}</dt>
                                <dd>未激活session</dd>
                            </dl>
                        </div>
                    </el-col>
                    <el-col :span="5">
                        <div class="serve_top_char_80 mr10">
                            <dl class="top_font_10">
                                <dt class="serve_name">{{process_num}}</dt>
                                <dd>进程数量</dd>
                            </dl>
                        </div>
                    </el-col>
                    <el-col :span="4">
                        <div class="serve_top_char_80 mr10">
                            <dl class="top_font_10">
                                <dt class="serve_name">{{failed_jobs}}</dt>
                                <dd>失败作业数</dd>
                            </dl>
                        </div>
                    </el-col>
                    <el-col :span="5">
                        <div class="serve_top_char_80">
                            <dl class="top_font_10">
                                <dt class="serve_name">{{rman_failed}}</dt>
                                <dd>失败备份数</dd>
                            </dl>
                        </div>
                    </el-col>
                </el-col>
                <!--<el-col :span="9">
                    <div type="flex" class="row-bg serve_top_left" justify="space-around">
                        <OracleTablespaceUsage :id="oracleTablespaceUsage" :data="oracleTablespaceUsageData"></OracleTablespaceUsage>
                    </div>
                </el-col>-->
            </el-row>
            <el-row class="serve_center">
                <el-col :span="12">
                    <div  class="serve_center_left ">
                        <p>Process Usage</p>
                        <linegraph :id="'bargrapOracleProcessUsage'" :data="optionOracleProcessUsage" class="linegraph_oracle"></linegraph>
                    </div>
                </el-col>
                <el-col :span="12" >
                    <div class="serve_center_right mr10">
                        <p>Session Usage</p>
                        <linegraph :id="'bargraphOracleSessionUsage'" :data="optionOracleSessionUsage" class="linegraph_oracle"></linegraph>
                    </div>
                </el-col>
            </el-row>
            <el-row :span="24">
                <div class="serve_bottom">
                    <p>数据文件</p>
                    <OracleDataFile :id="oracleDataFileList" :data="oracleDataFileData"></OracleDataFile>
                </div>
            </el-row>
            <el-row :span="24">
                <div class="serve_bottom">
                    <p>日志文件</p>
                    <OracleLogFile :id="oracleLogFileList" :data="oracleLogFileData"></OracleLogFile>
                </div>
            </el-row>
            <el-row :span="24">
                <div class="serve_bottom">
                    <p>控制文件</p>
                    <OracleControlFile :id="oracleControlFileList" :data="oracleControlFileData"></OracleControlFile>
                </div>
            </el-row>
            <el-row :span="24">
                <div class="serve_bottom">
                    <p>消耗CPU最多SQL</p>
                    <OracleCpuSql :id="oracleCpuSqlList" :data="oracleCpuSqlData"></OracleCpuSql>
                </div>
            </el-row>
            <el-row  :span="24" >
                <div class="serve_bottom">
                    <p>消耗内存最多SQL</p>
                    <OracleMemSql :id="oracleMemSqlList" :data="oracleMemSqlData"></OracleMemSql>
                </div>
            </el-row>
        </div>
    </div>

</template>
<script>
    import OracleHitRatio from './oracleEchart/OracleHitRatio';
    import OracleSgaRate from './oracleEchart/OracleSgaRate';
    import OraclePgaRate from './oracleEchart/OraclePgaRate';
    import OracleCpuSql from "./oracleEchart/OracleCpuSql";
    import OracleMemSql from "./oracleEchart/OracleMemSql";
    // import OracleTablespaceUsage from "./oracleEchart/OracleTablespaceUsage";
    import linegraph from '../network_equipment/visualNetworkEchart/MinutesCpuUtilization.vue';
    import OracleDataFile from "./oracleEchart/OracleDataFile";
    import OracleControlFile from "./oracleEchart/OracleControlFile";
    import OracleLogFile from "./oracleEchart/OracleLogFile";

    export default {
        name: 'ViewServe',
        components: {
            OracleHitRatio,
            OracleSgaRate,
            OraclePgaRate,
            OracleCpuSql,
            OracleMemSql,
            // OracleTablespaceUsage,
            OracleDataFile,
            OracleControlFile,
            OracleLogFile,
            linegraph
        },
        data(){
            return{
                hit_ratio_use:'hit_ratio_use',
                hit_ratio_data: 0,
                sga_rate_use:'sga_rate_use',
                sga_rate_data:0,
                pga_rate_use:'pga_rate_use',
                pga_rate_data:0,
                instance_name:'',
                star_time:'',
                serveIp:'',
                version:'',
                active_session_count: 0,
                inactive_session_count: 0,
                process_num: 0,
                failed_jobs: 0,
                rman_failed: 0,

                oracleCpuSqlList:'oracleCpuSqlList',
                oracleCpuSqlData:[],

                oracleMemSqlList:'oracleMemSqlList',
                oracleMemSqlData:[],

                oracleTablespaceUsage:'oracleTablespaceUsage',
                oracleTablespaceUsageData: [],

                oracleDataFileList:'oracleDataFileList',
                oracleDataFileData: [],

                oracleLogFileList:'oracleLogFileList',
                oracleLogFileData: [],

                oracleControlFileList:'oracleControlFileList',
                oracleControlFileData: [],

                optionOracleProcessUsage:{
                    title:'',
                    legendData:[],
                    xAxisData:[],
                    seriesData:[],
                    animation:true
                },
                optionOracleSessionUsage:{
                    title:'',
                    legendData:[],
                    xAxisData:[],
                    seriesData:[],
                    animation:true
                },
                monitorTime:[],
                oracleData:[],
                oracleDatabase:'',
            }
        },
        computed: {
        },
        created() {
            this.monitorTime=[this.Format(new Date()-12*60*60*1000), this.Format(new Date())];
            this.queryOneOracle();
            this.timer=setInterval(()=>{this.changeQueryHost();},180000);
        },
        mounted() {
        },
        methods: {
            queryOneOracle(){
                this.$http.get(`monitor/api/databases/?db_type=ORACLE&current_page=1&pre_page=1&is_monitor=是`, {
                    headers: {'token':localStorage.getItem('token')}
                }).then((res) => {
                    const oneOracleData = res.data;
                    const ip=oneOracleData.data[0].ip_address;
                    const sid=oneOracleData.data[0].sid;
                    this.oracleDatabase=sid+'/'+ip;
                    this.optionData(ip,sid);
                    const curTime=Date.parse(this.monitorTime[1])/1000;
                    const startTime=Date.parse(this.monitorTime[0])/1000;
                    this.query_history(startTime,curTime,ip);
                }).catch( (error)=> {
                    this.$message.error(JSON.stringify(error.response.data.detail));
                });
            },
            queryOracleDB(query){
                if (query !== '') {
                    this.$http.get(`monitor/api/databases/search?db_type=ORACLE&query=${query}&is_monitor=是`, {
                        headers: {'token':localStorage.getItem('token')}
                    }).then((res) => {
                        this.oracleData = res.data;
                    }).catch( (error)=> {
                        this.$message.error(JSON.stringify(error.response.data.detail));
                    });
                } else {
                    this.optionsNetworkIp = [];
                }
            },
            changeQueryHost(){
                const curTime=Date.parse(this.monitorTime[1])/1000;
                const startTime=Date.parse(this.monitorTime[0])/1000;
                const db_name=this.oracleDatabase.split('/');
                const db_sid=db_name[0];
                const db_ip=db_name[1];
                this.optionData(db_ip,db_sid);
                this.query_history(startTime,curTime, db_ip);
            },
			getJsonObjLength(jsonObj) {
				var Length = 0;
				for (const item in jsonObj) {
					console.log(item);
					Length++;
				}
				return Length;
			},
            optionData(db_ip,db_sid){
                this.$http.get(`monitor/api/databases/monitor/?db_name=ORACLE_${db_ip}_${db_sid}`, {
                    headers:{'token': this.token}
                }).then((res)=>{
					const jslength=this.getJsonObjLength(res.data);
					
					if(jslength<=3){
						this.serveIp=res.data.LOGIC_IP;
						this.star_time='';
						this.version = '';
						this.instance_name = res.data.INSTALL_NAME;
						this.hit_ratio_data=0;
						this.sga_rate_data=0;
						this.pga_rate_data=0;
						
						this.active_session_count = 0;
						this.inactive_session_count = 0;
						this.process_num = 0;
						this.failed_jobs = 0;
						this.rman_failed = 0;
						
						this.oracleCpuSqlData=[];
						this.oracleMemSqlData=[];
						this.oracleTablespaceUsageData = [];
						this.oracleDataFileData = [];
						this.oracleLogFileData = [];
						this.oracleControlFileData = [];
					}else{
						this.serveIp=res.data.LOGIC_IP;
						this.star_time=this.Format(res.data.INSTANCE.STARTUP_TIME);
						this.version = res.data.INSTANCE.VERSION;
						this.instance_name = res.data.INSTANCE.INSTANCE_NAME;
						this.hit_ratio_data=Math.round(res.data.HIT_RATIO.split('%')[0])/100;
						this.sga_rate_data=Math.round(res.data.SGA_USED_RATE.split('%')[0])/100;
						this.pga_rate_data=Math.round(res.data.PGA_USED_RATE.split('%')[0])/100;
						
						this.active_session_count = res.data.ACTIVE_SESSION_COUNT;
						this.inactive_session_count = res.data.INACTIVE_SESSION_COUNT;
						this.process_num = res.data.PROCESS_NUM;
						this.failed_jobs = res.data.FAILED_JOBS;
						this.rman_failed = res.data.FAILED;
						this.oracleCpuSqlData=res.data.SQL_PHYSICAL_IO;
						this.oracleMemSqlData=res.data.SQL_LOGIC_IO;
						this.oracleTablespaceUsageData = res.data.TABLESPACE_USAGE;
						this.oracleDataFileData = res.data.DATA_FILE;
						this.oracleLogFileData = res.data.LOG_FILE;
						this.oracleControlFileData = res.data.CONTROL_FILE;
					}
                    

                }).catch( (error) => {
                    this.$message.error(JSON.stringify(error.response.data.detail));
                });
            },
            query_history(startTime,curTime, ip){
                this.$http.get(`monitor/api/databases/history/?start=`+startTime+`&end=`+curTime+`&m=sum:PROCESSES_USAGE{logicIp=${ip}}`, {
                    headers:{'token': this.token}
                }).then((res)=>{
                    const lineTime=Object.keys(res.data);
                    const lineXtime=[];
                    for(let item in lineTime){
                        lineXtime.push(this.Format(lineTime[item]*1000));
                    }
                    const linevla=Object.values(res.data);
                    this.optionOracleProcessUsage.xAxisData=lineXtime;
                    this.optionOracleProcessUsage.seriesData=[{
                        name: "Process Usage",
                        type: "line",
                        smooth: true,
                        symbol: 'circle',
                        symbolSize: 3,
                        lineStyle: {
                            normal: {
                                color:'#a86ad1'
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
                                    offset: 0, color: 'rgba(168,106,209, 0.9)' // 0% 处的颜色
                                }, {
                                    offset: 0.8, color: 'rgba(168,106,209, 0)' // 100% 处的颜色
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
                    console.log(error);
                    this.$message.error(JSON.stringify(error.response.data.detail));
                });

                this.$http.get(`monitor/api/databases/history/?start=`+startTime+`&end=`+curTime+`&m=sum:SESSIONS_USAGE{logicIp=${ip}}`, {
                    headers:{
                        'token': this.token
                    }
                }).then((res)=>{
                    const lineTime=Object.keys(res.data);
                    const lineXtime=[];
                    for(let item in lineTime){
                        lineXtime.push(this.Format(lineTime[item]*1000));
                    }
                    const linevla=Object.values(res.data);
                    this.optionOracleSessionUsage.xAxisData=lineXtime;
                    this.optionOracleSessionUsage.seriesData=[{
                        name: "Session Usage",
                        type: "line",
                        smooth: true,
                        symbol: 'circle',
                        symbolSize: 3,
                        lineStyle: {
                            normal: {
                                color:'#c6375b'
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
                                    offset: 0, color: 'rgba(198,55,91, 0.9)' // 0% 处的颜色
                                }, {
                                    offset: 0.8, color: 'rgba(198,55,91, 0)' // 100% 处的颜色
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
                    console.log(error);
                    this.$message.error(JSON.stringify(error.response.data.detail));
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
                return y + '-' + MM + '-' + d + ' ' + h + ':' + m+':'+s ;

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
    .linegraph_oracle{
        height: 170px;
    }
    .serve_top_left,.serve_top_char{
        height:120px;
        background:#24273e;
        border-radius: 10px;
    }
    .serve_top_char_80{
        height:80px;
        background:#24273e;
        border-radius: 10px;
    }
    .serve_bottom{
        margin:10px;
        height:330px;
        background:#24273e;
        border-radius: 10px;
    }
    .serve_center_left,.serve_center_right{
        height:200px;
        background:#24273e;
        border-radius: 10px;
    }
    .serve_center_left{
        margin:0 10px 0 10px;
    }
    .serve_top{
        height:120px;
    }
    .serve_top_80{
        height:80px;
    }
    .serve_center,.serve_bottom{
        p{
            color:#03c2ec;
            font-size:12px;
            padding:10px 0 0 10px;
            font-weight: 600;
        }
    }
    .mb10{
        margin-bottom:10px;
    }
</style>







