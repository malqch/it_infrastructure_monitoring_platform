<template>
    <div class="brand-container">
        <el-container class="wrap">
            <el-header class="head">
                <el-row type="flex" class="row-bg" justify="space-between">
                    <el-col :span="8"></el-col>
                    <el-col :span="8">
                        <h2>IT基础设施统一监控</h2>
                    </el-col>
                    <el-col :span="8">
                        <el-dropdown class="sys">
                              <span class="el-dropdown-link sys-dropdown">
                              </span>
                            <el-dropdown-menu slot="dropdown">
                                <el-dropdown-item>
                                    <el-link type="primary" href="/#/sys" :push="2">
                                        系统管理
                                    </el-link>
                                </el-dropdown-item>
                                <el-dropdown-item>
                                    <el-link type="primary" href="/#/asset" :push="2">
                                        资产管理
                                    </el-link>
                                </el-dropdown-item>
                                <el-dropdown-item>
                                    <el-link type="primary" href="/#/monitor">
                                        集中监控管理平台
                                    </el-link>
                                </el-dropdown-item>
                                <el-dropdown-item>
                                    <el-link type="primary" href="/#/automation">
                                        自动化运维
                                    </el-link>
                                </el-dropdown-item>
                                <el-dropdown-item>
                                    <el-link type="primary" :href=this.globalAPI.elkUrl target="_blank">
                                        日志监控分析
                                    </el-link>
                                </el-dropdown-item>
                                <el-dropdown-item v-if="this.username==='admin'">
                                    <el-link type="primary" :href=this.globalAPI.nroUrl target="_blank">
                                        网络编排
                                    </el-link>
                                </el-dropdown-item>
                                <el-dropdown-item>
                                    <el-link type="primary" href="/#/login">
                                        退出登录
                                    </el-link>
                                </el-dropdown-item>
                            </el-dropdown-menu>
                        </el-dropdown>
                    </el-col>
                </el-row>
            </el-header>
            <el-main class="mainbox">
                <p class="title_p mb10">| 各类资产的数量统计</p>
                <el-row class="resume">
                    <div class="resume-bd mb10">
                        <el-row>
                            <el-col :span="6" class="center">
                                <i class="physical mlr10"></i>
                                <dl class="top_font_10">
                                    <dt class="time">{{physicalServeNum}}</dt>
                                    <dd>物理服务器</dd>
                                </dl>
                            </el-col>
                            <el-col :span="6" class="center">
                                <i class="virtual mlr10"></i>
                                <dl class="top_font_10">
                                    <dt class="time">{{virtualServerNum}}</dt>
                                    <dd>虚拟服务器</dd>
                                </dl>
                            </el-col>
                            <el-col :span="6" class="center">
                                <i class="storage mlr10"></i>
                                <dl class="top_font_10">
                                    <dt class="time">{{storageNum}}</dt>
                                    <dd>存储</dd>
                                </dl>
                            </el-col>
                            <el-col :span="6" class="center">
                                <i class="router mlr10"></i>
                                <dl class="top_font_10">
                                    <dt class="time">{{routerNum}}</dt>
                                    <dd>路由器</dd>
                                </dl>
                            </el-col>
                        </el-row>
                       <el-row class="mt10">
                           <el-col :span="6" class="center">
                               <i class="firewall mlr10"></i>
                               <dl class="top_font_10">
                                   <dt class="time">{{firewallNum}}</dt>
                                   <dd>防火墙</dd>
                               </dl>
                           </el-col>
                           <el-col :span="6" class="center">
                               <i class="switch mlr10"></i>
                               <dl class="top_font_10">
                                   <dt class="time">{{switchNum}}</dt>
                                   <dd>交换机</dd>
                               </dl>
                           </el-col>
                           <el-col :span="6" class="center">
                               <i class="database mlr10"></i>
                               <dl class="top_font_10">
                                   <dt class="time">{{databaseNum}}</dt>
                                   <dd>数据库</dd>
                               </dl>
                           </el-col>
                           <el-col :span="6" class="center">
                               <i class="middle mlr10"></i>
                               <dl class="top_font_10">
                                   <dt class="time">{{middlewareNum}}</dt>
                                   <dd>中间件</dd>
                               </dl>
                           </el-col>
                       </el-row>

                    </div>
                </el-row>
                <el-row class="mt10">
                    <el-col :span="7">
                        <div class="panel mr10">
                            <p class="title_p mt10 ml10">cpuTOP3</p>
                            <div class="chartdDiv">
                                <lineEcharts :id="'cpuTopn'" :data="cpuData" class="ech_height"></lineEcharts>
                            </div>
                        </div>

                        <div class="panel mr10 mt10">
                            <p class="title_p mt10 ml10">内存TOP3</p>
                            <lineEcharts :id="'memTopn'" :data="memData" class="ech_height"></lineEcharts>
                        </div>
                    </el-col>
                    <el-col :span="11">
                        <div class="app-main">
                            <!-- <p class="title_p">拓扑图</p> -->
							<el-tabs type="border-card" >
								<el-tab-pane label="广域网">

									<topologyWeb></topologyWeb>
								</el-tab-pane>
								<el-tab-pane label="互联网">
									<topology></topology>
								</el-tab-pane>
							</el-tabs>

                        </div>
                    </el-col>
                    <el-col :span="6">
                        <div class="panel ml10 botm_right">
                            <p class="title_p mt10 ml10 mb10">告警</p>
                            <div class="mt10">
                                <el-row class="mt10">
                                    <el-col :span="5" class="center">
                                        <dl>
                                            <dt class="white">提示</dt>
                                            <dd class="time hint"> {{hintNum}} </dd>
                                        </dl>
                                    </el-col>
                                    <el-col :span="5" class="center">
                                        <dl>
                                            <dt class="white">报警</dt>
                                            <dd class="time orange">{{reportNum}} </dd>
                                        </dl>
                                    </el-col>
                                    <el-col :span="5" class="center">
                                        <dl>
                                            <dt class="white">重要</dt>
                                            <dd class="time reds"> {{importNum}} </dd>
                                        </dl>
                                    </el-col>
                                    <el-col :span="5" class="center">
                                        <dl>
                                            <dt class="white">严重</dt>
                                            <dd class="time yellow">{{badlyNum}} </dd>
                                        </dl>
                                    </el-col>
                                    <el-col :span="4" class="center">
                                        <dl>
                                            <dt class="white">紧急</dt>
                                            <dd class="time red">{{urgencyNum}} </dd>
                                        </dl>
                                    </el-col>
                                    <!--<el-col :span="4" class="center">
                                        <dl>
                                            <dt class="white">所有</dt>
                                            <dd class="time"> {{total}} </dd>
                                        </dl>
                                    </el-col>-->
                                </el-row>
                                <div class="warnDiv">
                                    <ul>
                                        <li v-for="(item,index) in warnData" :key="index" :class="item.iconClass">
                                            <p>{{item.info}}</p>
                                            <p class="warn_time_p">{{item.time}}</p>
                                        </li>
                                    </ul>
                                </div>
                            </div>

                        </div>
                    </el-col>
                </el-row>
            </el-main>
        </el-container>
    </div>

</template>

<script>
    import lineEcharts from "../../application/echart/Line.vue";
    import topology from './topology/physical_topology_seciences.vue';
	import topologyWeb from './topology/physical_topology_seciences_web.vue';
    export default {
        name: 'Brand',
        components: {
            lineEcharts,
            topology,
			topologyWeb
        },
        data() {
            return {
                cpuData:{
                    lengedData:'',
                    xAxisData:[],
                    seriesData:[],
                    animation:true
                },
                memData:{
                    lengedData:'',
                    xAxisData:[],
                    seriesData:[],
                    animation:true
                },
                physicalServeNum:0,
                virtualServerNum:0,
                storageNum:0,
                firewallNum:0,
                switchNum:0,
                databaseNum:0,
                middlewareNum:0,
                routerNum:0,
                warnData:[],
                importNum:0,
                urgencyNum:0,
//                total:0,
                hintNum:0,
                reportNum:0,
                badlyNum:0,
                timer:null
            }
        },
        computed: {
            username() {
                let username = localStorage.getItem('username');
                return username ? username : this.name;
            }
        },
        created() {
        },
        mounted() {
            this.initQueryData();
            this.timer=setInterval(()=>{
                this.cpuData.animation=false;
                this.memData.animation=false;
                this.initQueryData();
            },60000)

        },
        methods: {
            initQueryData(){
                this.$http.get(`monitor/api/middleware/count`, {
                    headers:
                        {'token':localStorage.getItem('token')}
                }).then((res) => {
                    if(res.data!=null){
                        this.databaseNum=res.data.database_count[0].value;
                        this.middlewareNum=res.data.middleware_count[0].value;
                    }
                }).catch( (error)=> {
                    this.$message.error(JSON.stringify(error.response.data));
                });
                this.$http.get(`asset/api/device/visualization`, {
                    headers:
                        {'token':localStorage.getItem('token')}
                }).then((res) => {
                    if(res.data!=null){
                        if(res.data.server_data.length!=0){
                            res.data.server_data.map( item =>{
                                if(item.device_type=='服务器'){
                                    this.physicalServeNum=item.device_type__count;
                                }else if(item.device_type=='虚拟服务器'){
                                    this.virtualServerNum=item.device_type__count;
                                }
                            })
                        }
                        if(res.data.asset_info.length!=0){
                            res.data.asset_info.map( item=>{
                                if(item.device_type=='防火墙'){
                                    this.firewallNum=item.device_type__count;
                                }else if(item.device_type=='路由器'){
                                    this.routerNum=item.device_type__count;
                                }else if(item.device_type=='交换机'){
                                    this.switchNum=item.device_type__count;
                                }else if(item.device_type=='存储'){
                                    this.storageNum=item.device_type__count;
                                }
                            })
                        }
                    }
                }).catch( (error)=> {
                    this.$message.error(JSON.stringify(error.response.data));
                });
                this.$http.get(`monitor/api/alarm_detail/alarm_count`, {
                    headers:
                        {'token':localStorage.getItem('token')}
                }).then((res) => {
                    if(res.data!=null){
                        if(res.data.remain_alarm_detail!=undefined || res.data.remain_alarm_detail.length!=0){
                            res.data.level_count.map( item=>{
                                if(item.name=='5'){
                                    this.urgencyNum=item.value;
                                }else if(item.name=='4'){
                                    this.badlyNum=item.value;
                                }else if(item.name=='3'){
                                    this.importNum=item.value;
                                }else if(item.name=='2'){
                                    this.reportNum=item.value;
                                }else if(item.name=='1'){
                                    this.hintNum=item.value;
                                 }
                            })
                        }
                        if(res.data.remain_alarm_detail!=undefined || res.data.remain_alarm_detail.length!=0){
                            this.warnData=res.data.remain_alarm_detail.map( item =>{
                                const warnObj={};
                                warnObj.info=`${item.server_type}${item.alarm_ip}发生${item.alarm_level}告警`;
                                warnObj.time=item.alarm_last_time;
                                const icon=item.alarm_level=='提示' ? 'hint_icon' : item.alarm_level=='报警' ? 'warn_icon' : item.alarm_level=='重要' ? 'import_icon':item.alarm_level=='严重' ? 'badly_icon' : 'urgency_icon';
                                warnObj.iconClass=icon;
                                return warnObj;
                            });
                        }
//                    this.total=res.data.total_count[0].value;
                    }
                }).catch( (error)=> {
                    console.log(error);
                    this.$message.error(JSON.stringify(error.response.data));
                });
                this.$http.get(`monitor/api/analysis/history/?m=CPU_PERCENT`, {
                    headers:
                        {'token':localStorage.getItem('token')}
                }).then((res) => {
                    if(res.data!=null || res.data.length!=0){
                        const lengedData=[];
                        res.data.map( item =>{ return lengedData.push(item.name)});
                        this.cpuData.lengedData=lengedData;
                        const chartsTime=res.data[0].data;
                        const changeChartsTime=Object.keys(chartsTime);
                        let xAxis=changeChartsTime.map( item =>{
                            return this.Format(item*1000);
                        });
                        this.cpuData.xAxisData=xAxis;
                        /*this.cpuData.seriesData=[{
                         name: res.data[0].name,
                         type: 'line',
                         // smooth: true, //是否平滑
                         //                        showAllSymbol: true,
                         symbol: 'circle',
                         symbolSize: 10,
                         label: {
                         show: true,
                         position: 'top',
                         textStyle: {
                         color: '#00ca95',
                         }
                         },
                         itemStyle: {
                         color: "#00ca95",
                         borderColor: "#fff",
                         borderWidth: 3,
                         shadowColor: 'rgba(0, 0, 0, .3)',
                         shadowBlur: 0,
                         shadowOffsetY: 2,
                         shadowOffsetX: 2,
                         },
                         areaStyle: {
                         normal: {
                         color: new this.$echarts.graphic.LinearGradient(0, 0, 0, 1, [{
                         offset: 0,
                         color: 'rgba(0,202,149,0.3)'
                         },
                         {
                         offset: 1,
                         color: 'rgba(0,202,149,0)'
                         }
                         ], false),
                         shadowColor: 'rgba(0,202,149,0.9)',
                         shadowBlur: 20
                         }
                         },
                         data: Object.values(res.data[0].data)
                         },
                         {
                         name: res.data[1].name,
                         type: 'line',
                         // smooth: true, //是否平滑
                         //                        showAllSymbol: true,
                         symbol: 'circle',
                         symbolSize: 10,
                         label: {
                         show: true,
                         position: 'top',
                         textStyle: {
                         color: 'orange',
                         }
                         },
                         itemStyle: {
                         color: "#ef8101",
                         borderColor: "#fff",
                         borderWidth: 3,
                         shadowColor: 'rgba(0, 0, 0, .3)',
                         shadowBlur: 0,
                         shadowOffsetY: 2,
                         shadowOffsetX: 2,
                         },
                         areaStyle: {
                         normal: {
                         color: new this.$echarts.graphic.LinearGradient(0, 0, 0, 1, [{
                         offset: 0,
                         color: 'rgba(239,129,1,0.3)'
                         },
                         {
                         offset: 1,
                         color: 'rgba(239,129,1,0)'
                         }
                         ], false),
                         shadowColor: 'rgba(239,129,1,0.9)',
                         shadowBlur: 20
                         }
                         },
                         data: Object.values(res.data[1].data)
                         },
                         {
                         name: res.data[2].name,
                         type: 'line',
                         // smooth: true, //是否平滑
                         //                        showAllSymbol: true,
                         symbol: 'circle',
                         symbolSize: 10,
                         label: {
                         show: true,
                         position: 'top',
                         textStyle: {
                         color: '#orange',
                         }
                         },
                         itemStyle: {
                         color: "#6c50f3",
                         borderColor: "#fff",
                         borderWidth: 3,
                         shadowColor: 'rgba(0, 0, 0, .3)',
                         shadowBlur: 0,
                         shadowOffsetY: 2,
                         shadowOffsetX: 2,
                         },
                         areaStyle: {
                         normal: {
                         color: new this.$echarts.graphic.LinearGradient(0, 0, 0, 1, [{
                         offset: 0,
                         color: 'rgba(108,80,243,0.3)'
                         },
                         {
                         offset: 1,
                         color: 'rgba(108,80,243,0)'
                         }
                         ], false),
                         shadowColor: 'rgba(108,80,243,0.9)',
                         shadowBlur: 20
                         }
                         },
                         data: Object.values(res.data[2].data)
                         }];*/
                        this.cpuData.seriesData=[{
                            name: res.data[0].name,
                            type: 'line',
                            // smooth: true, //是否平滑
//                        showAllSymbol: true,
                            symbol: 'circle',
                            symbolSize: 10,
                            label: {
                                show: true,
                                position: 'top',
                                textStyle: {
                                    color: '#00ca95',
                                }
                            },
                            itemStyle: {
                                color: "#00ca95",
                                borderColor: "#fff",
                                borderWidth: 3,
                                shadowColor: 'rgba(0, 0, 0, .3)',
                                shadowBlur: 0,
                                shadowOffsetY: 2,
                                shadowOffsetX: 2,
                            },
                            areaStyle: {
                                normal: {
                                    color: new this.$echarts.graphic.LinearGradient(0, 0, 0, 1, [{
                                        offset: 0,
                                        color: 'rgba(0,202,149,0.3)'
                                    },
                                        {
                                            offset: 1,
                                            color: 'rgba(0,202,149,0)'
                                        }
                                    ], false),
                                    shadowColor: 'rgba(0,202,149,0.9)',
                                    shadowBlur: 20
                                }
                            },
                            data: Object.values(res.data[0].data)
                        },
                            {
                                name: res.data[1].name,
                                type: 'line',
                                // smooth: true, //是否平滑
//                        showAllSymbol: true,
                                symbol: 'circle',
                                symbolSize: 10,
                                label: {
                                    show: true,
                                    position: 'top',
                                    textStyle: {
                                        color: 'orange',
                                    }
                                },
                                itemStyle: {
                                    color: "#ef8101",
                                    borderColor: "#fff",
                                    borderWidth: 3,
                                    shadowColor: 'rgba(0, 0, 0, .3)',
                                    shadowBlur: 0,
                                    shadowOffsetY: 2,
                                    shadowOffsetX: 2,
                                },
                                areaStyle: {
                                    normal: {
                                        color: new this.$echarts.graphic.LinearGradient(0, 0, 0, 1, [{
                                            offset: 0,
                                            color: 'rgba(239,129,1,0.3)'
                                        },
                                            {
                                                offset: 1,
                                                color: 'rgba(239,129,1,0)'
                                            }
                                        ], false),
                                        shadowColor: 'rgba(239,129,1,0.9)',
                                        shadowBlur: 20
                                    }
                                },
                                data: Object.values(res.data[1].data)
                            },
                            {
                                name: res.data[2].name,
                                type: 'line',
                                // smooth: true, //是否平滑
//                        showAllSymbol: true,
                                symbol: 'circle',
                                symbolSize: 10,
                                label: {
                                    show: true,
                                    position: 'top',
                                    textStyle: {
                                        color: '#orange',
                                    }
                                },
                                itemStyle: {
                                    color: "#6c50f3",
                                    borderColor: "#fff",
                                    borderWidth: 3,
                                    shadowColor: 'rgba(0, 0, 0, .3)',
                                    shadowBlur: 0,
                                    shadowOffsetY: 2,
                                    shadowOffsetX: 2,
                                },
                                areaStyle: {
                                    normal: {
                                        color: new this.$echarts.graphic.LinearGradient(0, 0, 0, 1, [{
                                            offset: 0,
                                            color: 'rgba(108,80,243,0.3)'
                                        },
                                            {
                                                offset: 1,
                                                color: 'rgba(108,80,243,0)'
                                            }
                                        ], false),
                                        shadowColor: 'rgba(108,80,243,0.9)',
                                        shadowBlur: 20
                                    }
                                },
                                data: Object.values(res.data[2].data)
                            }];
                    }
                }).catch( (error)=> {
                    this.$message.error(JSON.stringify(error.response.data));
                });
                this.$http.get(`monitor/api/analysis/history/?m=MEM_PERCENT`, {
                    headers:
                        {'token':localStorage.getItem('token')}
                }).then((res) => {
                    if(res.data!=null || res.data.length!=0){
                        const lengedData=[];
                        res.data.map( item =>{ return lengedData.push(item.name)});
                        this.memData.lengedData=lengedData;
                        const chartsTime=res.data[0].data;
                        const changeChartsTime=Object.keys(chartsTime);
                        let xAxis=changeChartsTime.map( item =>{
                            return this.Format(item*1000);
                        });
                        this.memData.xAxisData=xAxis;
                        this.memData.seriesData=[{
                            name: res.data[0].name,
                            type: 'line',
                            // smooth: true, //是否平滑
//                        showAllSymbol: true,
                            symbol: 'circle',
                            symbolSize: 10,
                            label: {
                                show: true,
                                position: 'top',
                                textStyle: {
                                    color: '#00ca95',
                                }
                            },
                            itemStyle: {
                                color: "#00ca95",
                                borderColor: "#fff",
                                borderWidth: 3,
                                shadowColor: 'rgba(0, 0, 0, .3)',
                                shadowBlur: 0,
                                shadowOffsetY: 2,
                                shadowOffsetX: 2,
                            },
                            areaStyle: {
                                normal: {
                                    color: new this.$echarts.graphic.LinearGradient(0, 0, 0, 1, [{
                                        offset: 0,
                                        color: 'rgba(0,202,149,0.3)'
                                    },
                                        {
                                            offset: 1,
                                            color: 'rgba(0,202,149,0)'
                                        }
                                    ], false),
                                    shadowColor: 'rgba(0,202,149,0.9)',
                                    shadowBlur: 20
                                }
                            },
                            data: Object.values(res.data[0].data)
                        },
                            {
                                name: res.data[1].name,
                                type: 'line',
                                // smooth: true, //是否平滑
//                        showAllSymbol: true,
                                symbol: 'circle',
                                symbolSize: 10,
                                label: {
                                    show: true,
                                    position: 'top',
                                    textStyle: {
                                        color: '#orange',
                                    }
                                },
                                itemStyle: {
                                    color: "#ef8101",
                                    borderColor: "#fff",
                                    borderWidth: 3,
                                    shadowColor: 'rgba(0, 0, 0, .3)',
                                    shadowBlur: 0,
                                    shadowOffsetY: 2,
                                    shadowOffsetX: 2,
                                },
                                areaStyle: {
                                    normal: {
                                        color: new this.$echarts.graphic.LinearGradient(0, 0, 0, 1, [{
                                            offset: 0,
                                            color: 'rgba(239,129,1,0.3)'
                                        },
                                            {
                                                offset: 1,
                                                color: 'rgba(239,129,1,0)'
                                            }
                                        ], false),
                                        shadowColor: 'rgba(239,129,1,0.9)',
                                        shadowBlur: 20
                                    }
                                },
                                data: Object.values(res.data[1].data)
                            },
                            {
                                name: res.data[2].name,
                                type: 'line',
                                // smooth: true, //是否平滑
//                        showAllSymbol: true,
                                symbol: 'circle',
                                symbolSize: 10,
                                label: {
                                    show: true,
                                    position: 'top',
                                    textStyle: {
                                        color: '#orange',
                                    }
                                },
                                itemStyle: {
                                    color: "#6c50f3",
                                    borderColor: "#fff",
                                    borderWidth: 3,
                                    shadowColor: 'rgba(0, 0, 0, .3)',
                                    shadowBlur: 0,
                                    shadowOffsetY: 2,
                                    shadowOffsetX: 2,
                                },
                                areaStyle: {
                                    normal: {
                                        color: new this.$echarts.graphic.LinearGradient(0, 0, 0, 1, [{
                                            offset: 0,
                                            color: 'rgba(108,80,243,0.3)'
                                        },
                                            {
                                                offset: 1,
                                                color: 'rgba(108,80,243,0)'
                                            }
                                        ], false),
                                        shadowColor: 'rgba(108,80,243,0.9)',
                                        shadowBlur: 20
                                    }
                                },
                                data: Object.values(res.data[2].data)
                            }];
                    }
                }).catch( (error)=> {
                    this.$message.error(JSON.stringify(error.response.data));
                });


               /* this.memData.xAxisColor='#6c50f3',
                this.memData.xAxisData=['10.10.10.6','10.10.10.3','10.10.10.4','10.10.10.130','10.10.10.132'];
                this.memData.seriesData=[{
                    name: '利用率',
                    type: 'line',
                    // smooth: true, //是否平滑
//                        showAllSymbol: true,
                    symbol: 'circle',
                    symbolSize: 10,
                    label: {
                        show: true,
                        position: 'top',
                        textStyle: {
                            color: '#6c50f3',
                        }
                    },
                    itemStyle: {
                        color: "#6c50f3",
                        borderColor: "#fff",
                        borderWidth: 3,
                        shadowColor: 'rgba(0, 0, 0, .3)',
                        shadowBlur: 0,
                        shadowOffsetY: 2,
                        shadowOffsetX: 2,
                    },
                    areaStyle: {
                        normal: {
                            color: new this.$echarts.graphic.LinearGradient(0, 0, 0, 1, [{
                                offset: 0,
                                color: 'rgba(108,80,243,0.3)'
                            },
                                {
                                    offset: 1,
                                    color: 'rgba(108,80,243,0)'
                                }
                            ], false),
                            shadowColor: 'rgba(108,80,243, 0.9)',
                            shadowBlur: 20
                        }
                    },
                    data: [502.84, 205.97, 332.79, 281.55, 398.35, 214.02, ]
                }];*/

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
                return y + '-' + MM + '-' + d + ' ' + h + ':' + m +':'+ s ;

            }
        },
        beforeDestroy() {
            clearInterval(this.timer);
            this.timer = null;
        }
    }
</script>

<style lang="scss" scoped>
    @import "../../assets/css/fonts/font.css";
    @import "../../assets/scss/echarts";
    .app-main {
        /*height: calc(100vh - 50px)!important;*/
        height: 502px;
        scrollbar-width:none; /* Firefox */
        -ms-overflow-style: none; /* IE 10+ */
    }
    ::-webkit-scrollbar {
        display: none; /* Chrome Safari */
    }
    dl{
        display:inline-block;
        dt.white{
            color:#d9faf7;
            font-size: 14px;
            font-weight: 600;
        }
    }
    .center{
        text-align: center;
    }
    .physical,.virtual,.storage,.router,.firewall,.switch,.database,.middle{
        width:35px;
        height:33px;
        display: inline-block;
    }
    .physical{
        width: 28px;
        background: url('../../assets/img/index/physical.png')no-repeat;
        background-size: contain;
    }
    .virtual{
        background: url('../../assets/img/index/virtual.png')no-repeat;
        background-size: contain;
    }
    .storage{
        background: url('../../assets/img/index/storage.png')no-repeat;
        background-size: contain;
    }
    .router{
        background: url('../../assets/img/index/router.png')no-repeat;
        background-size: contain;
    }
    .firewall{
        background: url('../../assets/img/index/firewall.png')no-repeat;
        background-size: contain;
    }
    .switch{
        width: 28px;
        background: url('../../assets/img/index/switch.png')no-repeat;
        background-size: contain;
    }
    .database{
        width: 28px;
        background: url('../../assets/img/index/database.png')no-repeat;
        background-size: contain;
    }
    .middle{
        width: 28px;
        background: url('../../assets/img/index/middle.png')no-repeat;
        background-size: contain;
    }
    html,body{
        width:100%;
        height:100%;
    }
    .brand-container {
        position: absolute;
        width: 100%;
        height: 100%;
        background: #000;
        .wrap {
            background: url('../../assets/img/index/true.png') no-repeat;
            background-size: cover;
            line-height: 1.15;
            height:100%;
            .head{
                position: relative;
                height: 1rem;
                background: url('../../assets/img/index/head_bg_1.png') no-repeat top center;
                background-size: 100% 100%;
                .sys-dropdown{
                    background: url('../../assets/img/index/sys.png') no-repeat top center;
                    background-size: 100% 100%;
                    width:40px;
                    height:33px;
                    display: inline-block;
                    margin-top:3px;
                }
                .sys{
                    margin-left:90%;
                }
                h2{
                    color: #7ef0ff;
                    font-size: 26px;
                    text-align: center;
                    line-height: 50px;
                    letter-spacing: 2px;
                }
                /*.showTime {
                    position: absolute;
                    right: 1.375rem;
                    top: 0.5rem;
                    color: rgba(126, 240, 255, .7);
                    display: flex;
                    .time {
                        font-size: .28rem;
                        margin-right: .18rem;
                    }
                    .date {
                        span {
                            display: block;
                            &:nth-child(1) {
                                font-size: .12rem;
                                text-align: right;
                            }
                            &:nth-child(2) {
                                font-size: .14rem;
                            }
                        }
                    }
                }*/
            }
            .mainbox {
                /*min-width: 1024px;
                max-width: 1920px;*/
                /*padding: 0.125rem 0.125rem 0;*/
                padding:10px 20px 0 20px;
                /*overflow: hidden;*/
                /*display: flex;*/
                /*&.center {
                    !*flex: 5;*!
                    margin: 0 0.125rem 0.1rem;
                    overflow: hidden;

                }*/
                .resume {
                    .resume-bd {
                        /*background: rgba(57, 74, 129, 0.1);*/
                        position: relative;
                        border: 1px solid rgba(25, 186, 139, 0.17);
                        border-bottom-left-radius: 55px;
                        border-top-right-radius: 55px;
                        height:145px;
                        dl{
                            margin-left: 15px;
                        }
                        dd,dt{
                            color:#b3ccf8;
                        }
                        dt{
                            font-size: 30px;
                        }
                        dd{
                            margin-top: 0;
                        }
                        &:before {
                            content: "";
                            position: absolute;
                            width: 30px;
                            height: 10px;
                            border-top: 2px solid #02a6b5;
                            border-left: 2px solid #02a6b5;
                            top: 0;
                            left: 0;
                        }
                        &:after {
                            content: "";
                            position: absolute;
                            width: 30px;
                            height: 10px;
                            border-bottom: 2px solid #02a6b5;
                            border-right: 2px solid #02a6b5;
                            right: 0;
                            bottom: 0;
                        }
                    }

                }
                .panel {
                    position: relative;
                    /*height: 3.875rem;*/
                    border: 1px solid rgba(25, 186, 139, 0.09);
                    /*background: rgba(255, 255, 255, 0.04) url('../../assets/img/index/line.png');*/
                    padding: 0 0.1875rem 0;
                    &:before {
                        position: absolute;
                        top: 0;
                        left: 0;
                        content: "";
                        width: 10px;
                        height: 10px;
                        border-top: 2px solid #02a6b5;
                        border-left: 2px solid #02a6b5;
                    }
                    &:after {
                        position: absolute;
                        top: 0;
                        right: 0;
                        content: "";
                        width: 10px;
                        height: 10px;
                        border-top: 2px solid #02a6b5;
                        border-right: 2px solid #02a6b5;
                    }
                    .panel-footer {
                        position: absolute;
                        left: 0;
                        bottom: 0;
                        width: 100%;
                        &:before {
                            position: absolute;
                            bottom: 0;
                            left: 0;
                            content: "";
                            width: 10px;
                            height: 10px;
                            border-bottom: 2px solid #02a6b5;
                            border-left: 2px solid #02a6b5;
                        }
                        &:after {
                            position: absolute;
                            bottom: 0;
                            right: 0;
                            content: "";
                            width: 10px;
                            height: 10px;
                            border-bottom: 2px solid #02a6b5;
                            border-right: 2px solid #02a6b5;
                        }
                    }
                    h4 {
                        height: 0.6rem;
                        line-height: 0.6rem;
                        text-align: center;
                        color: #fff;
                        font-size: 0.225rem;
                        font-weight: 400;
                        a {
                            margin: 0 0.1875rem;
                            color: #fff;
                            text-decoration: none;
                        }
                    }
                    .chart {
                        height: 3rem;
                    }

                    ul{
                        margin-left:60px;
                        li{
                            color:#b3ccf8;
                            font-size: 12px;
                            letter-spacing: 1px;
                            .warn_time_p{
                                color:#a1b0cc;
                                margin-top: 5px;
                            }
                        }

                    }
                }

            }

        }

    }
    .title_p{
        color:#2db7c4;
        font-size:12px;
        font-weight: 600;
    }
    .botm_right{
        height: 500px;
    }
    .center{
        text-align: center;
        h5{
            color: #d8fffd;
        }
    }
    ul,li{
        list-style: none;
    }
    .red{
        color: #ff2613;
    }
    .yellow{
        color: #f15800
    }
    .orange{
        color: #f9f05c;
    }
    .reds{
       color: #f0a720;
    }
    .hint{
        color: #f9f4d3;
    }
    .warn_icon{
        &:before{
            width: 20px;
            height: 20px;
            content: '';
            background: url('../../assets/img/index/warn.png')no-repeat left;
            background-size: 100%;
            display: inline-block;
            position: relative;
            left: -30px;
            top: 23px;
        }
    }
    .import_icon{
        &:before{
            width: 20px;
            height: 20px;
            content: '';
            background: url('../../assets/img/index/_import.png')no-repeat left;
            background-size: 100%;
            display: inline-block;
            position: relative;
            left: -30px;
            top: 23px;
        }
    }
    .hint_icon{
        &:before{
            width: 20px;
            height: 20px;
            content: '';
            background: url('../../assets/img/index/hint.png')no-repeat left;
            background-size: 100%;
            display: inline-block;
            position: relative;
            left: -30px;
            top: 23px;
        }
    }
    .badly_icon{
        &:before{
            width: 20px;
            height: 20px;
            content: '';
            background: url('../../assets/img/index/badly.png')no-repeat left;
            background-size: 100%;
            display: inline-block;
            position: relative;
            left: -30px;
            top: 23px;
        }
    }
    .urgency_icon{
        &:before{
            width: 20px;
            height: 20px;
            content: '';
            background: url('../../assets/img/index/urgency.png')no-repeat left;
            background-size: 100%;
            display: inline-block;
            position: relative;
            left: -30px;
            top: 23px;
        }
    }
    .warnDiv{
        overflow: auto;
        height: 380px;
        scrollbar-width:none; /* Firefox */
        -ms-overflow-style: none; /* IE 10+ */
    }
    ::-webkit-scrollbar {
        display: none; /* Chrome Safari */
    }
    .chartdDiv{
        width:100%;
        height:100%;
    }
    .ech_height{
        height:220px;
        /*height:100%;*/
    }

    .el-dropdown-menu,.el-dropdown-menu__item{
        background-color: #152642;
        border:1px solid #152642;
    }
    /deep/ .el-link.el-link--primary{
        color:#33b0c0;
    }
    /deep/ .el-dropdown-menu__item:not(.is-disabled):hover{
        background-color:#1B3456;
    }
     .el-popper /deep/ .popper__arrow{
        border-bottom-color:#132645;
         top: -8px;
    }
     .el-popper /deep/  .popper__arrow::after{
         border-bottom-color:#132645;
    }
    .el-dropdown-menu{
        box-shadow: 0 4px 14px 0 rgb(4, 7, 15);
    }


    /*@media screen and (max-width:1024px) {
        html {
            font-size: 42px !important;
        }
    }
    @media screen and (min-width:1280px) {
        html {
            font-size: 46px !important;
        }
    }
    @media screen and (min-width:1920px) {
        html {
            font-size: 80px !important;
        }
    }*/
	/deep/ .el-tabs--border-card {
		background: none;
		border: none;
		color: #fff;
		box-shadow: none;
		height: 100%;
	}
	/deep/ .el-tab-pane{
		background: #0c1f33;
	}
	/deep/ .el-tabs--border-card>.el-tabs__content {
		padding: 15px 0!important;
		height: calc(100% - 70px);
	}
	/deep/ .el-tabs--border-card>.el-tabs__header {
		background-color: #094154;
		border-bottom: none;
	}

	/deep/ .el-tabs--border-card>.el-tabs__header .el-tabs__item {
		color: #03c2ec;
		border: none;
	}

	/deep/ .el-tabs--border-card>.el-tabs__header .el-tabs__item.is-active {
		color: #e6a23c;
		background-color: #356b7d;
		border: none;
	}
	/deep/ .main_view{
		overflow:hidden;
		height: 100%;
	}
	/deep/ .el-tab-pane{
		height:100%;
		margin-left: -20px;
	}
</style>
