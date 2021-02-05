<template>
    <div>
        <div class="wrapper">
            <el-row class="serve_select">
                <el-form ref="form" label-width="100px">
                    <el-col :span="9">
                        <el-form-item label="IP">
                            <el-select
                                    v-model="fireWallIp"
                                    filterable
                                    remote
                                    reserve-keyword
                                    placeholder="请输入IP"
                                    :remote-method="queryHost"
                                    @change="changeQueryHost">
                                <el-option
                                        v-for="(item) in ipData"
                                        :key=item.id
                                        :label=item.ipaddr
                                        :value="item.ipaddr+'/'+item.name">
                                </el-option>
                            </el-select>
                        </el-form-item>
                    </el-col>
                    <el-col :span="4" v-show="isShowName">
                        <div class="mt5 center">
                            设备名称:<span id="isShowName">{{deviceName}}</span>
                        </div>
                    </el-col>
                    <el-col :span="11">
                        <el-form-item label="起止日期">
                            <el-date-picker
                                    v-model="storageTime"
                                    type="datetimerange"
                                    range-separator="至"
                                    start-placeholder="开始日期"
                                    end-placeholder="结束日期"
                                    @change="changeQueryHost">
                            </el-date-picker>
                        </el-form-item>
                    </el-col>
                </el-form>
            </el-row>
            <el-row :span="24" class="mlr10 mt10">
                <el-col :span="4">
                    <div class="mr10">
                        <el-row>
                            <div class="network_top_top">
                                <dl class="top_font_10 mlr10">
                                    <dt class="time">{{storageIp}}</dt>
                                    <dd>IP</dd>
                                </dl>
                            </div>
                        </el-row>
                        <el-row>
                            <div class="network_top_top mtb10">
                                <dl class="top_font_10">
                                    <dt class="serve_name_18">{{serviceType}}</dt>
                                    <dd>交换机</dd>
                                </dl>
                            </div>
                        </el-row>
                        <el-row>
                            <div class="network_top_top">
                                <dl class="top_font_10">
                                    <dt class="serve_name_18">{{seriesName}}</dt>
                                    <dd>系列名称</dd>
                                </dl>
                            </div>
                        </el-row>
                        <el-row>
                            <div class="network_top_top mt10">
                                <dl class="top_font_10">
                                    <dt class="serve_name_18">{{vendorName}}</dt>
                                    <dd>厂商</dd>
                                </dl>
                            </div>
                        </el-row>
                    </div>
                </el-col>
                <el-col :span="20">
                    <div class="mb10">
                        <el-row>
                            <el-col :span="6">
                                <div class="network_top_top">
                                    <dl class="top_font_10 mlr10">
                                        <dt class="time">{{MmsSessionsVal}}</dt>
                                        <dd>{{MmsSessions}}</dd>
                                    </dl>
                                </div>
                            </el-col>
                            <el-col :span="6">
                                <div class="network_top_top ml10">
                                    <dl class="top_font_10">
                                        <dt class="time">{{MgcpSessionsVal}}</dt>
                                        <dd>{{MgcpSessions}}</dd>
                                    </dl>
                                </div>
                            </el-col>
                            <el-col :span="6">
                                <div class="network_top_top ml10">
                                    <dl class="top_font_10">
                                        <dt class="time">{{IlsSessionsVal}}</dt>
                                        <dd>{{IlsSessions}}</dd>
                                    </dl>
                                </div>
                            </el-col>
                            <el-col :span="6">
                                <div class="network_top_top ml10">
                                    <dl class="top_font_10">
                                        <dt class="time">{{CurSessSpeedVal}}</dt>
                                        <dd>{{CurSessSpeed}}</dd>
                                    </dl>
                                </div>
                            </el-col>
                        </el-row>
                        <el-row>
                            <el-col :span="6">
                                <div class="network_top_top mr10 mt10">
                                    <dl class="top_font_10">
                                        <dt class="time">{{H323SessionsVal}}</dt>
                                        <dd>{{H323Sessions}}</dd>
                                    </dl>
                                </div>
                            </el-col>
                            <el-col :span="6">
                                <div class="network_top_top">
                                    <dl class="top_font_10 mt10">
                                        <dt class="time">{{MonUdpSessVal}}</dt>
                                        <dd>{{MonUdpSess}}</dd>
                                    </dl>
                                </div>
                            </el-col>
                            <el-col :span="6">
                                <div class="network_top_top ml10 mt10">
                                    <dl class="top_font_10">
                                        <dt class="time">{{DnsSessionsVal}}</dt>
                                        <dd>{{DnsSessions}}</dd>
                                    </dl>
                                </div>
                            </el-col>
                            <el-col :span="6">
                                <div class="network_top_top mt10 ml10">
                                    <dl class="top_font_10">
                                        <dt class="time">{{TotalSessVal}}</dt>
                                        <dd>{{TotalSess}}</dd>
                                    </dl>
                                </div>
                            </el-col>
                        </el-row>
                        <el-row>
                            <el-col :span="6">
                                <div class="network_top_top mt10 mr10">
                                    <dl class="top_font_10">
                                        <dt class="time">{{HwccSessionsVal}}</dt>
                                        <dd>{{HwccSessions}}</dd>
                                    </dl>
                                </div>
                            </el-col>
                            <el-col :span="6">
                                <div class="network_top_top mt10">
                                    <dl class="top_font_10">
                                        <dt class="time">{{HttpSessionsVal}}</dt>
                                        <dd>{{HttpSessions}}</dd>
                                    </dl>
                                </div>
                            </el-col>
                            <el-col :span="6">
                                <div class="network_top_top mt10 ml10">
                                    <dl class="top_font_10">
                                        <dt class="time">{{FtpSessionsVal}}</dt>
                                        <dd>{{FtpSessions}}</dd>
                                    </dl>
                                </div>
                            </el-col>
                            <el-col :span="6">
                                <div class="network_top_top mt10 ml10">
                                    <dl class="top_font_10">
                                        <dt class="time">{{Throughput64Val}}</dt>
                                        <dd>{{Throughput64}}</dd>
                                    </dl>
                                </div>
                            </el-col>
                        </el-row>
                        <el-row>
                            <el-col :span="5">
                                <div class="network_top_top mt10 mr10">
                                    <dl class="top_font_10">
                                        <dt class="time">{{SmtpSessionsVal}}</dt>
                                        <dd>{{SmtpSessions}}</dd>
                                    </dl>
                                </div>
                            </el-col>
                            <el-col :span="5">
                                <div class="network_top_top mt10">
                                    <dl class="top_font_10">
                                        <dt class="time">{{RcvIcmpPktsVal}}</dt>
                                        <dd>{{RcvIcmpPkts}}</dd>
                                    </dl>
                                </div>
                            </el-col>
                            <el-col :span="5">
                                <div class="network_top_top mt10 ml10">
                                    <dl class="top_font_10">
                                        <dt class="time">{{RcvTcpPktsVal}}</dt>
                                        <dd>{{RcvTcpPkts}}</dd>
                                    </dl>
                                </div>
                            </el-col>
                            <el-col :span="5">
                                <div class="network_top_top mt10 ml10">
                                    <dl class="top_font_10">
                                        <dt class="time">{{ThroughputVal}}</dt>
                                        <dd>{{Throughput}}</dd>
                                    </dl>
                                </div>
                            </el-col>
                            <el-col :span="4">
                                <div class="network_top_top mt10 ml10">
                                    <dl class="top_font_10">
                                        <dt class="time">{{PortScanDropPktsVal}}</dt>
                                        <dd>{{PortScanDropPkts}}</dd>
                                    </dl>
                                </div>
                            </el-col>
                        </el-row>
                    </div>
                </el-col>
            </el-row>
            <el-row class="mlr10 mb10">
                <el-col :span="4">
                    <div class="network_top_top mr10">
                        <dl class="top_font_10">
                            <dt class="time">{{TotalBootConnNumVal}}</dt>
                            <dd>{{TotalBootConnNum}}</dd>
                        </dl>
                    </div>
                </el-col>
                <el-col :span="4">
                    <div class="network_top_top">
                        <dl class="top_font_10">
                            <dt class="time">{{RtspSessionsVal}}</dt>
                            <dd>{{RtspSessions}}</dd>
                        </dl>
                    </div>
                </el-col>
                <el-col :span="4">
                    <div class="network_top_top mlr10">
                        <dl class="top_font_10">
                            <dt class="time">{{TcpSessVal}}</dt>
                            <dd>{{TcpSess}}</dd>
                        </dl>
                    </div>
                </el-col>
                <el-col :span="4">
                    <div class="network_top_top">
                        <dl class="top_font_10">
                            <dt class="time">{{RcvUdpPktsVal}}</dt>
                            <dd>{{RcvUdpPkts}}</dd>
                        </dl>
                    </div>
                </el-col>
                <el-col :span="4">
                    <div class="network_top_top  ml10">
                        <dl class="top_font_10">
                            <dt class="time">{{RcvFragPktsVal}}</dt>
                            <dd>{{RcvFragPkts}}</dd>
                        </dl>
                    </div>
                </el-col>
                <el-col :span="4">
                    <div class="network_top_top ml10">
                        <dl class="top_font_10">
                            <dt class="time">{{AllPktsVal}}</dt>
                            <dd>{{AllPkts}}</dd>
                        </dl>
                    </div>
                </el-col>
            </el-row>
            <el-row class="serve_center">
                <el-row :span="24" class="network_cpu">
                    <el-col :span="8" v-for="(item,index) in optionsData" :key="index" class="chart-item-area">
                        <cpuUtilization
                                :data="item"
                                :id='"charts" +index'
                                :index="index"
                                class="linegraph_firewall"
                        ></cpuUtilization>
                    </el-col>
                </el-row>

            </el-row>
        </div>
    </div>
</template>
<script>
    import cpuUtilization from './visualNetworkEchart/MinutesCpuUtilization.vue';
//    import portStatus from './visualNetworkEchart/portStatus.vue';

    export default {
        name: 'ViewNetwork',
        components: {
            cpuUtilization
//            portStatus
        },
        data(){
            return{
                timer:null,
                chartList:[],
                optionsData:[],
                storageIp:'',
                serviceType:'',
                seriesName:0,
                vendorName:'',

                MmsSessionsVal:'',
                MmsSessions:'',
                MgcpSessionsVal:'',
                MgcpSessions:'',
                IlsSessionsVal:'',
                IlsSessions:'',
                DnsSessionsVal:'',
                DnsSessions:'',
                H323SessionsVal:'',
                H323Sessions:'',
                MonUdpSessVal:'',
                MonUdpSess:'',
                HwccSessionsVal:'',
                HwccSessions:'',
                HttpSessionsVal:'',
                HttpSessions:'',
                FtpSessionsVal:'',
                FtpSessions:'',
                TotalSessVal:'',
                TotalSess:'',
                SmtpSessionsVal:'',
                SmtpSessions:'',
                RtspSessionsVal:'',
                RtspSessions:'',
                TcpSessVal:'',
                TcpSess:'',
                CurSessSpeedVal:'',
                CurSessSpeed:'',
                TotalBootConnNumVal:'',
                TotalBootConnNum:'',
                AllPktsVal:'',
                AllPkts:'',
                RcvUdpPktsVal:'',
                RcvUdpPkts:'',
                RcvIcmpPktsVal:'',
                RcvIcmpPkts:'',
                PortScanDropPktsVal:'',
                PortScanDropPkts:'',
                Throughput64Val:'',
                Throughput64:'',
                ThroughputVal:'',
                Throughput:'',
                RcvFragPktsVal:'',
                RcvFragPkts:'',
                RcvTcpPktsVal:'',
                RcvTcpPkts:'',

                storageTime:[],
                portStatusData:null,
                portTotal:0,
                loading: false,
                optionsNetworkIp:[],
                ipList:[],
                fireWallIp:'',
                ipData:[],
                isShowName:true,
                deviceName:''
            }
        },
        computed: {
        },
        created() {
            this.storageTime=[this.Format(new Date()-12*60*60*1000), this.Format(new Date())];
            const url  = window.document.location.href;
            const search=url.split('?');
            if(search[1]==undefined){
                this.queryOneIp();
            }else{
                const search_ips=search[1].split('&');
                const search_ip=search_ips[0].split('=');
                this.fireWallIp=search_ip[1];
                const search_name=search_ips[2].split('=');
                this.deviceName=search_name[1];
                const start=this.storageTime[0].replace(/-/g,'/').replace(/\s/g,'-');
                const end=this.storageTime[1].replace(/-/g,'/').replace(/\s/g,'-');
                this.serveHistory(start,end);
            }

        },
        mounted() {
            this.timer=setInterval(()=>{
                this.changeQueryHost();
            },300000);
        },
        methods: {
            queryHost(query){
                if (query !== '') {
                    this.$http.get(`asset/api/nro/network/network?query=${query}&device_type=FW&is_monitor=是`, {
                        headers:
                            {
                                'token': localStorage.getItem('token')
                            }
                    }).then((res) => {
                        this.ipData=res.data;
                    }).catch( (error) =>{
                        this.$message.error(JSON.stringify(error.response.data));
                    });
                } else {
                    this.optionsNetworkIp = [];
                }
            },
            queryOneIp(){
                this.$http.get(`asset/api/nro/network/?type=FW&current_page=1&pre_page=1&is_monitor=是`, {
                    headers:
                        {
                            'token':localStorage.getItem('token')
                        }
                }).then((res) => {
                    console.log(res.data.data[0].hostname);
                    this.fireWallIp=res.data.data[0].ipaddr;
                    this.deviceName=(res.data.data[0].hostname) ? res.data.data[0].hostname : res.data.data[0].name;
                    console.log('deviceName', this.deviceName);
                    const start=this.storageTime[0].replace(/-/g,'/').replace(/\s/g,'-');
                    const end=this.storageTime[1].replace(/-/g,'/').replace(/\s/g,'-');
                    this.serveHistory(start,end);
                }).catch( (error)=> {
                    this.$message.error(JSON.stringify(error.response.data));
                });
            },
            changeQueryHost(){
                this.optionsData=[];
                const ip_name=this.fireWallIp.split('/');
                this.fireWallIp=ip_name[0];
                this.deviceName=ip_name[1];
                const start=this.storageTime[0].replace(/-/g,'/').replace(/\s/g,'-');
                const end=this.storageTime[1].replace(/-/g,'/').replace(/\s/g,'-');
                this.serveHistory(start,end);
            },
            serveHistory(start,end){
                this.$http.get(`monitor/api/network_monitor/monitor/?network_name=FIREWALL_${this.fireWallIp}_${this.deviceName}`, {
                    headers:{
                        'token': this.token
                    }
                }).then((res)=>{
                    const resData=res.data;
                    if(resData.IFSPEED==undefined ){
                        this.$message.warning('未查到数据');
                        this.storageIp='';
                        this.serviceType='';
                        this.seriesName='';
                        this.vendorName='';

                        this.MmsSessionsVal='';
                        this.MmsSessions='';
                        this.MgcpSessionsVal='';
                        this.MgcpSessions='';
                        this.IlsSessionsVal='';
                        this.IlsSessions='';
                        this.DnsSessionsVal='';
                        this.DnsSessions='';
                        this.H323SessionsVal='';
                        this.H323Sessions='';
                        this.MonUdpSessVal='';
                        this.MonUdpSess='';
                        this.HwccSessionsVal='';
                        this.HwccSessions='';
                        this.HttpSessionsVal='';
                        this.HttpSessions='';
                        this.FtpSessionsVal='';
                        this.FtpSessions='';
                        this.TotalSessVal='';
                        this.TotalSess='';
                        this.SmtpSessionsVal='';
                        this.SmtpSessions='';
                        this.RtspSessionsVal='';
                        this.RtspSessions='';
                        this.TcpSessVal='';
                        this.TcpSess='';
                        this.CurSessSpeedVal='';
                        this.CurSessSpeed='';
                        this.TotalBootConnNumVal='';
                        this.TotalBootConnNum='';
                        this.AllPktsVal='';
                        this.AllPkts='';
                        this.RcvUdpPktsVal='';
                        this.RcvUdpPkts='';
                        this.RcvIcmpPktsVal='';
                        this.RcvIcmpPkts='';
                        this.PortScanDropPktsVal='';
                        this.PortScanDropPkts='';
                        this.Throughput64Val='';
                        this.Throughput64='';
                        this.ThroughputVal='';
                        this.Throughput='';
                        this.RcvFragPktsVal='';
                        this.RcvFragPkts='';
                        this.RcvTcpPktsVal='';
                        this.RcvTcpPkts='';
                        return false;
                    }
                        this.storageIp=resData.HWSECSTATMONMMSSESSIONS.ip;
                        this.serviceType=resData.HWSECSTATMONMMSSESSIONS.serviceType;
                        this.seriesName=resData.HWSECSTATMONMMSSESSIONS.seriesName;
                        this.vendorName=resData.HWSECSTATMONMMSSESSIONS.vendorName;

                        this.MmsSessionsVal=resData.HWSECSTATMONMMSSESSIONS.indicatorValue;
                        this.MmsSessions=resData.HWSECSTATMONMMSSESSIONS.indicatorName;
                        this.MgcpSessionsVal=resData.HWSECSTATMONMGCPSESSIONS.indicatorValue;
                        this.MgcpSessions=resData.HWSECSTATMONMGCPSESSIONS.indicatorName;
                        this.IlsSessionsVal=resData.HWSECSTATMONILSSESSIONS.indicatorValue;
                        this.IlsSessions=resData.HWSECSTATMONILSSESSIONS.indicatorName;
                        this.DnsSessionsVal=resData.HWSECSTATMONDNSSESSIONS.indicatorValue;
                        this.DnsSessions=resData.HWSECSTATMONDNSSESSIONS.indicatorName;
                        this.H323SessionsVal=resData.HWSECSTATMONH323SESSIONS.indicatorValue;
                        this.H323Sessions=resData.HWSECSTATMONH323SESSIONS.indicatorName;
                        this.MonUdpSessVal=resData.HWSECSTATMONUDPSESS.indicatorValue;
                        this.MonUdpSess=resData.HWSECSTATMONUDPSESS.indicatorName;
                        this.HwccSessionsVal=resData.HWSECSTATMONHWCCSESSIONS.indicatorValue;
                        this.HwccSessions=resData.HWSECSTATMONHWCCSESSIONS.indicatorName;
                        this.HttpSessionsVal=resData.HWSECSTATMONHTTPSESSIONS.indicatorValue;
                        this.HttpSessions=resData.HWSECSTATMONHTTPSESSIONS.indicatorName;
                        this.FtpSessionsVal=resData.HWSECSTATMONFTPSESSIONS.indicatorValue;
                        this.FtpSessions=resData.HWSECSTATMONFTPSESSIONS.indicatorName;
                        this.TotalSessVal=resData.HWSECSTATMONTOTALSESS.indicatorValue;
                        this.TotalSess=resData.HWSECSTATMONTOTALSESS.indicatorName;
                        this.SmtpSessionsVal=resData.HWSECSTATMONSMTPSESSIONS.indicatorValue;
                       this.SmtpSessions=resData.HWSECSTATMONSMTPSESSIONS.indicatorName;
                        this.RtspSessionsVal=resData.HWSECSTATMONRTSPSESSIONS.indicatorValue;
                        this.RtspSessions=resData.HWSECSTATMONRTSPSESSIONS.indicatorName;
                        this.TcpSessVal=resData.HWSECSTATMONTCPSESS.indicatorValue;
                        this.TcpSess=resData.HWSECSTATMONTCPSESS.indicatorName;
                        this.CurSessSpeedVal=resData.HWSECSTATMONCURSESSSPEED.indicatorValue;
                        this.CurSessSpeed=resData.HWSECSTATMONCURSESSSPEED.indicatorName;
                        this.TotalBootConnNumVal=resData.HWSECSTATMONTOTALBOOTCONNNUM.indicatorValue;
                        this.TotalBootConnNum=resData.HWSECSTATMONTOTALBOOTCONNNUM.indicatorName;
                        this.AllPktsVal=resData.HWSECSTATMONALLPKTS.indicatorValue;
                        this.AllPkts=resData.HWSECSTATMONALLPKTS.indicatorName;
                        this.RcvUdpPktsVal=resData.HWSECSTATMONRCVUDPPKTS.indicatorValue;
                        this.RcvUdpPkts=resData.HWSECSTATMONRCVUDPPKTS.indicatorName;
                        this.RcvIcmpPktsVal=resData.HWSECSTATMONRCVICMPPKTS.indicatorValue;
                        this.RcvIcmpPkts=resData.HWSECSTATMONRCVICMPPKTS.indicatorName;
                        this.PortScanDropPktsVal=resData.HWSECSTATPORTSCANDROPPKTS.indicatorValue;
                        this.PortScanDropPkts=resData.HWSECSTATPORTSCANDROPPKTS.indicatorName;
                        this.Throughput64Val=resData.HWSECSTATDEVICETHROUGHPUT64.indicatorValue;
                        this.Throughput64=resData.HWSECSTATDEVICETHROUGHPUT64.indicatorName;
                        this.ThroughputVal=resData.HWSECSTATDEVICETHROUGHPUT.indicatorValue;
                        this.Throughput=resData.HWSECSTATDEVICETHROUGHPUT.indicatorName;
                        this.RcvFragPktsVal=resData.HWSECSTATMONRCVFRAGPKTS.indicatorValue;
                        this.RcvFragPkts=resData.HWSECSTATMONRCVFRAGPKTS.indicatorName;
                        this.RcvTcpPktsVal=resData.HWSECSTATMONRCVTCPPKTS.indicatorValue;
                        this.RcvTcpPkts=resData.HWSECSTATMONRCVTCPPKTS.indicatorName;
                    const portStatusArr=[];
                    for(let item in resData.port_status) {
                        portStatusArr.push({
                            portName: item,
                            portValue: resData.port_status[item]
                        })
                    }
                    this.portStatusData=portStatusArr;
                    this.portTotal=resData.IFSPEED.length;
                    for(let i=1;i<=this.portTotal;i++){
                        let chartListObj={};
                        chartListObj.title='port_'+i;
                        chartListObj.legendData=['流量'];
                        const ifSpeed='IFSPEED_'+i;
                        this.$http.get(`monitor/api/network_monitor/history/?start=`+start+`&end=`+end+`&m=`+ifSpeed+`&logic_ip=${this.fireWallIp}`, {
                            headers:{
                                'token': this.token
                            }
                        }).then( (res)=>{
                            const chartsTime=res.data.time;
                            let xAxis=chartsTime.map( item =>{
                                return this.Format(item*1000);
                            });
                            chartListObj.xAxisData=xAxis;

                            chartListObj.seriesData=[{
                                name: "流量",
                                type: "line",
                                smooth: true,
                                symbol: 'circle',
                                symbolSize: 3,
                                lineStyle: {
                                    normal: {
                                        color:'#16f892'
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
                                            offset: 0, color: 'rgba(22,248,146, 0.8)' // 0% 处的颜色
                                        }, {
                                            offset: 0.8, color: 'rgba(22,248,146, 0)' // 100% 处的颜色
                                        }],
                                        global: false // 缺省为 false
                                    },
                                    shadowColor: 'rgba(0, 0, 0, 0.1)',
                                    shadowBlur: 10
                                },
                                itemStyle: {
                                    normal: {
                                        color: '#16f892',
                                        borderColor: '#16f892'
                                    }
                                },
                                data:res.data[ifSpeed]
                            }];
                            this.optionsData.push(chartListObj);
                            this.optionsData.sort(function(a,b){
                                let port_num_a=a.title.split('_');
                                let port_num_b=b.title.split('_');
                                return port_num_a[1] - port_num_b[1];
                            });
                        }).catch( (error) => {
                            this.$message.error(JSON.stringify(error.response.data));
                        });
                    }
                }).catch( (error) => {
                    console.log(error);
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
    @import "../../../assets/css/fonts/font.css";
    @import "../../../assets/scss/echarts";
    .center{
        text-align: left;
        color: #fff;
        font-size: 14px;
    }
    .mt5{
        margin-top:5px;
    }
    .linegraph_firewall{
        height: 180px;
        padding: 6px 0;
    }
    .selectIp /deep/ .el-input__inner{
        color:#e5bb2e;
        font-size: 18px;
    }
    .network_top{
        border-radius: 10px;
        background:#24273e;
        height: 215px;
    }
    .network_top_top{
        border-radius: 10px;
        background:#24273e;
        height:55px
    }
    .network_cpu{
        margin:0 10px 10px 10px;
        background:#24273e;
        border-radius: 10px;
    }
    .serve_top_right{
        height: 70px;
        background: #24273e;
        border-radius: 8px;
        margin-top: 10px;
    }
    .textC{
        text-align: center;
    }
    .mt16{
        margin-top:16px;
    }
    .serve_top_mt{
        margin:10px 12px;
    }
    dl{
        dd{
            margin-top: 3px;
        }
    }
    .serve_center,.network_top{
        p{
            color:#03c2ec;
            font-size:12px;
            padding:10px 0 0 10px;
            font-weight: 600;
        }
    }
    .mt10{
        margin-top:10px;
    }
    .serve_name_18{
        font-size: 18px;
    }
    .top_font_10{
        padding-top:3px;
    }

</style>
