<template>
    <div>
        <div class="wrapper">
            <el-row class="serve_select">
                <el-form ref="form" label-width="100px">
                    <el-col :span="9">
                        <el-form-item label="Redis">
                            <el-select
                                    v-model="redisHost"
                                    filterable
                                    remote
                                    reserve-keyword
                                    placeholder="请输入服务器名称或IP"
                                    :remote-method="queryRedis"
                                    class="selectIp" @change="changeQueryHost">
                                <el-option
                                        v-for="(item) in redisData"
                                        :key=item.id
                                        :label="`${item.port}/${item.ip_address}`"
                                        :value="`${item.port}/${item.ip_address}`">
                                </el-option>
                            </el-select>
                        </el-form-item>
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
            <el-row class="serve_top" :gutter="10">
                <el-col :span="15" style="padding-left: 0;">
                    <el-col :span="10" style="padding-left: 0;">
                        <div class="mointor_top_left">
                            <dl class="top_redis">
                                <dt class="time">{{serveIp}}</dt>
                                <dd>服务器IP</dd>
                            </dl>
                        </div>
                    </el-col>
                    <el-col :span="8">
                        <div  class="mointor_top_left">
                            <dl class="top_redis">
                                <dt class="time">{{tcp_port}}</dt>
                                <dd>端口</dd>
                            </dl>
                        </div>
                    </el-col>
                    <el-col :span="6">
                        <div  class="mointor_top_left">
                            <dl class="top_redis">
                                <dt>{{role}}</dt>
                                <dd>角色</dd>
                            </dl>
                        </div>
                    </el-col>
                </el-col>
                <el-col :span="9" style="padding-left: 0;">
                    <el-col class="mointor_top_right">
                        <el-col :span="8" :offset="4">
                            <RedisMemDataPrec :id="dataset_prec_use" :data="dataset_prec_data"></RedisMemDataPrec>
                        </el-col>
                        <el-col :span="8" :offset="1">
                            <RedisMemPeakPrec :id="peak_prec_use" :data="peak_prec_data"></RedisMemPeakPrec>
                        </el-col>
                    </el-col>
                </el-col>
            </el-row>
            <el-row class="serve_bottom mtb10" :gutter="10">
                <el-col :span="5" class="serve_bottom_left">
                    <el-row class="mon_bot_top">
                        <dl class="top_font">
                            <dt>{{redis_mode}}</dt>
                            <dd>运行模式</dd>
                        </dl>
                    </el-row>
                    <el-row class="mon_bot_bot">
                        <dl class="top_font">
                            <dt class="time">{{uptime_in_days}}天</dt>
                            <dd>运行时间</dd>
                        </dl>
                    </el-row>
                </el-col>
                <el-col :span="19" class="serve_bottom_right">
                    <p>Redis参数信息</p>
                    <el-col :span="15">
                        <!-- <RedisDataTable :id="redis_table" :data="redis_table_data"></RedisDataTable> -->
						<el-table class="table-content" :data="redis_table_data" border height="235px" style="margin-top:10px">
							<el-table-column prop="name" label="名称" align="center">
							</el-table-column>
							<el-table-column prop="calls" label="calls" align="center">
							</el-table-column>
							<el-table-column prop="usec" label="usec" align="center">
							</el-table-column>
							<el-table-column prop="usec_per_call" label="usec_per_call" align="center">
							</el-table-column>
						</el-table>
                    </el-col>
                    <el-col :span="9">
                        <RedisList :id="redis_list" :data="redis_list_data"></RedisList>
                    </el-col>
                </el-col>
            </el-row>
            <el-row class="serve_center m10">
                <el-col :span="8">
                    <div class="serve_center_left">
                        <p>Input</p>
                        <RedisInput :id="'bargraphRedisInput'" :data="optionRedisInput" class="linegraph"></RedisInput>
                    </div>
                </el-col>
                <el-col :span="8">
                    <div class="serve_center_left mlr10">
                        <p>Output</p>
                        <RedisInput :id="'bargraphRedisOutput'" :data="optionRedisOutput" class="linegraph"></RedisInput>
                    </div>
                </el-col>
                <el-col :span="8">
                    <div class="serve_center_left">
                        <p>OPS</p>
                        <RedisInput :id="'bargraphRedisOps'" :data="optionRedisOps" class="linegraph"></RedisInput>
                    </div>
                </el-col>
            </el-row>
        </div>
    </div>
</template>
<script>
    import RedisInput from '../network_equipment/visualNetworkEchart/MinutesCpuUtilization.vue';
    import RedisMemDataPrec from './redisEchart/RedisMemDataPrec';
    import RedisMemPeakPrec from './redisEchart/RedisMemPeakPrec';
    //import RedisDataTable from './redisEchart/RedisDataTable';
    import RedisList from './redisEchart/redisList';

    export default {
        name: 'redisView',
        components: {
            RedisMemDataPrec,
            RedisMemPeakPrec,
            //RedisDataTable,
            RedisList,
            RedisInput,
        },
        data(){
            return{
                dataset_prec_use:'dataset_prec_use',
                dataset_prec_data: 0,
                peak_prec_use:'peak_prec_use',
                peak_prec_data:0,
                tcp_port:'',
                networkList:'networkList',
                networkListData:[],
                serveIp:'',
                redis_mode:'',
                role: '',
                uptime_in_days:'',
                redis_table:'redis_table',
                redis_table_data:[],
                redis_list:'redis_list',
                redis_list_data:[],
                redis_list_data_obj:'',

                optionRedisOps: {
                    title:'',
                    legendData:[],
                    xAxisData:[],
                    seriesData:[],
                    animation:true
                },

                optionRedisInput:{
                    title:'',
                    legendData:[],
                    xAxisData:[],
                    seriesData:[],
                    animation:true
                },
                optionRedisOutput: {
                    title:'',
                    legendData:[],
                    xAxisData:[],
                    seriesData:[],
                    animation:true
                },
                monitorTime:'',
                redisData:null,
                redisHost:'',
            }
        },
        computed: {
        },
        created() {
            this.monitorTime=[this.Format(new Date()-12*60*60*1000), this.Format(new Date())];
            this.queryOneRedis();
            this.timer=setInterval(()=>{this.changeQueryHost();},180000);
        },
        mounted() {
        },
        methods: {
            queryOneRedis(){
                this.$http.get(`monitor/api/middleware/?middleware_type=REDIS&current_page=1&pre_page=1&is_monitor=是`, {
                    headers: {'token':localStorage.getItem('token')}
                }).then((res) => {
                    const oneRedisData = res.data;
                    const ip=oneRedisData.data[0].ip_address;
                    const port=oneRedisData.data[0].port;
                    this.redisHost=port+'/'+ip;
                    this.optionData(ip,port);
                    const curTime=Date.parse(this.monitorTime[1])/1000;
                    const startTime=Date.parse(this.monitorTime[0])/1000;
                    this.serveHistory(startTime,curTime,ip);
                }).catch( (error)=> {
                    this.$message.error(JSON.stringify(error.response.data));
                });
            },
            queryRedis(query){
                if (query !== '') {
                    this.$http.get(`monitor/api/middleware/search?middleware_type=REDIS&query=${query}&is_monitor=是`, {
                        headers: {'token':localStorage.getItem('token')}
                    }).then((res) => {
                        this.redisData = res.data;
                    }).catch( (error)=> {
                        this.$message.error(JSON.stringify(error.response.data));
                    });
                } else {
                    this.optionsNetworkIp = [];
                }
            },
            changeQueryHost(){
                const curTime=Date.parse(this.monitorTime[1])/1000;
                const startTime=Date.parse(this.monitorTime[0])/1000;
                const redis_name=this.redisHost.split('/');
                const redis_port=redis_name[0];
                const redis_ip=redis_name[1];
                this.optionData(redis_ip,redis_port);
                this.serveHistory(startTime,curTime, redis_ip);
            },
            optionData(redis_ip,redis_port){
                this.$http.get(`monitor/api/middleware/monitor/?middleware_name=REDIS_${redis_ip}_${redis_port}`, {
                    headers:{'token': this.token}
                }).then((res)=>{
                    this.tcp_port=Number(res.data.TCP_PORT);
                    this.serveIp=res.data.LOGIC_IP;
                    this.uptime_in_days=Number(res.data.UPTIME_IN_DAYS);
                    this.redis_mode = res.data.REDIS_MODE;
                    this.role = res.data.ROLE;
                    this.dataset_prec_data=Math.round(res.data.USED_MEMORY_DATASET_PERC.split('%')[0])/100;
                    this.peak_prec_data=Math.round(res.data.USED_MEMORY_PEAK_PERC.split('%')[0])/100;
                    this.redis_list_data_obj = res.data;

                    // this.redis_table_data = [{
                    //     name: 'maxmemory_human',
                    //     value: res.data.MAXMEMORY_HUMAN
                    // },{
                    //     name: 'multiplexing_api',
                    //     value: res.data.MULTIPLEXING_API
                    // }, {
                    //     name: 'redis_mode',
                    //     value: res.data.REDIS_MODE
                    // }, {
                    //     name: 'redis_version',
                    //     value: res.data.REDIS_VERSION
                    // },{
                    //     name: 'used_memory_dataset_perc',
                    //     value: res.data.USED_MEMORY_DATASET_PERC
                    // },{
                    //     name: 'config_file',
                    //     value: res.data.CONFIG_FILE
                    // }, {
                    //     name: 'repl_backlog_histlen',
                    //     value: res.data.REPL_BACKLOG_HISTLEN
                    // }];
					this.redis_list_data=[];
					this.redis_table_data=[];
                    for(let i in this.redis_list_data_obj){
                        
						let obj=new Object();
						if(i.indexOf("CMDSTAT") != -1){
							obj.name=i;
							obj.calls=this.redis_list_data_obj[i].split(',')[0].split('=')[1];
							obj.usec=this.redis_list_data_obj[i].split(',')[1].split('=')[1];
							obj.usec_per_call=this.redis_list_data_obj[i].split(',')[2].split('=')[1];
							this.redis_table_data.push(obj)
						}else{
							this.redis_list_data.push({"name":i,"value":this.redis_list_data_obj[i]});
						}
                    }
					console.log(this.redis_table_data)
                }).catch( (error) => {
                    this.$message.error(JSON.stringify(error.response.data));
                });
            },
            serveHistory(startTime,curTime, redis_ip){
                this.$http.get(`monitor/api/middleware/history/?start=`+startTime+`&end=`+curTime+`&m=sum:INSTANTANEOUS_OPS_PER_SEC{logicIp=${redis_ip}}`, {
                    headers:{'token': this.token}
                }).then((res)=>{
                    const lineTime=Object.keys(res.data);
                    const lineXtime=[];
                    for(let item in lineTime){
                        lineXtime.push(this.Format(lineTime[item]*1000));
                    }
                    const linevla=Object.values(res.data);
                    this.optionRedisOps.xAxisData=lineXtime;
                    this.optionRedisOps.seriesData=[{
                        name: "Ops",
                        type: "line",
                        smooth: true,
                        symbol: 'circle',
                        symbolSize: 3,
                        lineStyle: {
                            normal: {
                                color:'#5a70d1'
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
                                    offset: 0, color: 'rgba(90,122,209, 0.9)' // 0% 处的颜色
                                }, {
                                    offset: 0.8, color: 'rgba(90,122,209, 0)' // 100% 处的颜色
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

                this.$http.get(`monitor/api/middleware/history/?start=`+startTime+`&end=`+curTime+`&m=sum:INSTANTANEOUS_INPUT_KBPS{logicIp=${redis_ip}}`, {
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
                    this.optionRedisInput.xAxisData=lineXtime;
                    this.optionRedisInput.seriesData=[{
                        name: "Input",
                        type: "line",
                        smooth: true,
                        symbol: 'circle',
                        symbolSize: 3,
                        lineStyle: {
                            normal: {
                                color:'#d1a056'
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
                                    offset: 0, color: 'rgba(209,160,86, 0.9)' // 0% 处的颜色
                                }, {
                                    offset: 0.8, color: 'rgba(209,160,86, 0)' // 100% 处的颜色
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

                this.$http.get(`monitor/api/middleware/history/?start=`+startTime+`&end=`+curTime+`&m=sum:INSTANTANEOUS_OUTPUT_KBPS{logicIp=${redis_ip}}`, {
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
                    this.optionRedisOutput.xAxisData=lineXtime;
                    this.optionRedisOutput.seriesData=[{
                        name: "Output",
                        type: "line",
                        smooth: true,
                        symbol: 'circle',
                        symbolSize: 3,
                        lineStyle: {
                            normal: {
                                color:'#68d156'
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
                                    offset: 0, color: 'rgba(70,209,51, 0.9)' // 0% 处的颜色
                                }, {
                                    offset: 0.8, color: 'rgba(70,209,51, 0)' // 100% 处的颜色
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
	@import "../../../assets/scss/darkStyle";
    .linegraph{
        height: 230px;
    }
    .serve_top{
        border-radius: 10px;
        margin:13px 10px!important;
    }
    .mointor_top_left{
        height:111px;
        border-radius: 10px;
        margin-right:0px;
        background:#24273e;
    }
	/deep/ .el-col{
		// padding-left: 0!important;
		// padding-right: 0!important;
	}
    .mointor_top_right{
        background:#24273e;
        height:111px;
        border-radius: 10px;
		padding-left: 0!important;
    }
	
    .serve_bottom_right{
        height:280px;
        background:#24273e;
        border-radius: 10px;
    }
    .serve_bottom_left{
        margin:0 0px 0 0px;
		padding-right: 10px!important;
    }
    .serve_center_left{
        height:280px;
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
	.serve_bottom{
		margin-left: 5px!important;
		margin-right: 10px!important;
	}
    .top_redis{
        text-align: center;
        padding-top: 28px;
    }
    .mon_bot_top{
        height: 130px;
        border-radius: 10px;
        margin-bottom:10px;
        background:#24273e;
    }
    .mon_bot_bot{
        height: 138px;
        border-radius: 10px;
        background:#24273e;
    }
	/deep/ .el-table__body-wrapper::-webkit-scrollbar {
		width: 5px;
		height: 6px;
		background: #191b2a;
	}
	
	/deep/ .el-table__body-wrapper::-webkit-scrollbar-thumb {
		background-color: #596077;
		border-radius: 2px;
	}
	
	/deep/.el-table th {
		background-color: #2c2f49 !important;
		color: #b08ff9;
		font-weight: normal;
	}
	
	/deep/ .el-table--border th {
		border-right: 1px solid #2c2f49;
		border-bottom: 1px solid #2c2f49;
	}
	
	/deep/ .el-table td {}
	
	/deep/ .el-table--border td {
		border-right: 1px solid #24273e;
		border-bottom: 1px solid #24273e;
	}
	
	/deep/ .el-table--enable-row-hover .el-table__body tr:hover>td {
		background: #24273e !important;
	}
	
	/deep/ .el-table tr {
		color: #fff;
		background: #24273e;
	}
	
	/deep/ .el-table--border th.gutter:last-of-type {
		border-bottom: none;
	}
	
	/deep/ .el-table--border th {
		border-right: none;
	}
	
	/deep/.el-table--small td {
		padding: 2px 0;
	}
	
	/deep/ .el-table--small th {
		padding: 5px 0;
	}
	
	/deep/ .el-table .sort-caret.ascending {
		border-bottom-color: #24273e;
		top: 5px;
	}
	
	/deep/ .el-table .sort-caret.descending {
		border-top-color: #24273e;
		bottom: 7px;
	}
	
	/deep/ .el-table__empty-block {
		background: #24273e;
	}
</style>







