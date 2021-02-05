<template>
    <div>
        <div class="wrapper">
            <el-row class="serve_select">
                <el-form ref="form" label-width="100px">
                    <el-col :span="9">
                        <el-form-item label="RabbitMQ">
                            <el-select
                                    v-model="rabbitMQHost"
                                    filterable
                                    remote
                                    reserve-keyword
                                    placeholder="请输入服务器名称或IP"
                                    :remote-method="queryRabbitMQ"
                                    class="selectIp" @change="changeQueryHost">
                                <el-option
                                        v-for="(item) in rabbitMQData"
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
            <el-row class="serve_top mb10">
                <el-col :span="24">
                    <el-col :span="6">
                        <div class="serve_top_char_ip ml10">
                            <dl class="top_font">
                                <dt class="time">{{serveIp}}</dt>
                                <dd>服务器IP</dd>
                            </dl>
                        </div>
                    </el-col>
                    <el-col :span="18">
                        <el-row>
                            <el-col :span="6">
                                <div class="serve_top_char mlr10">
                                    <dl class="top_font_wb">
                                        <dt class="time">{{mq_channels}}</dt>
                                        <dd>信道数量</dd>
                                    </dl>
                                </div>
                            </el-col>
                            <el-col :span="6">
                                <div class="serve_top_char">
                                    <dl class="top_font_wb">
                                        <dt class="time">{{mq_connections}}</dt>
                                        <dd>连接数量</dd>
                                    </dl>
                                </div>
                            </el-col>
                            <el-col :span="6">
                                <div class="serve_top_char ml10">
                                    <dl class="top_font_wb">
                                        <dt class="time">{{mq_consumers}}</dt>
                                        <dd>消费者数量</dd>
                                    </dl>
                                </div>
                            </el-col>
                            <el-col :span="6">
                                <div class="serve_top_char mlr10">
                                    <dl class="top_font_wb">
                                        <dt class="time">{{mq_exchanges}}</dt>
                                        <dd>交换机数量</dd>
                                    </dl>
                                </div>
                            </el-col>
                        </el-row>
                        <el-row class="mt10">
                            <el-col :span="6">
                                <div class="serve_top_char ml10">
                                    <dl class="top_font_wb">
                                        <dt class="time">{{mq_disk_reads}}</dt>
                                        <dd>读取消息总次数</dd>
                                    </dl>
                                </div>
                            </el-col>
                            <el-col :span="6">
                                <div class="serve_top_char mlr10">
                                    <dl class="top_font_wb">
                                        <dt class="time">{{mq_disk_writes}}</dt>
                                        <dd>写入消息总次数</dd>
                                    </dl>
                                </div>
                            </el-col>
                            <el-col :span="6">
                                <div class="serve_top_char">
                                    <dl class="top_font_wb">
                                        <dt class="time">{{mq_messages}}</dt>
                                        <dd>消息数量</dd>
                                    </dl>
                                </div>
                            </el-col>
                            <el-col :span="6">
                                <div class="serve_top_char mlr10">
                                    <dl class="top_font_wb">
                                        <dt class="time">{{mq_queues}}</dt>
                                        <dd>队列数量</dd>
                                    </dl>
                                </div>
                            </el-col>
                        </el-row>
                    </el-col>
                </el-col>
            </el-row>
            <el-row class="serve_center">
                <el-col :span="12">
                    <div  class="serve_center_left">
                        <p>磁盘读</p>
                        <linegraph :id="'diskReadRate_id'" :data="diskReadRateData" class="linegraph"></linegraph>
                    </div>
                </el-col>
                <el-col :span="12" >
                    <div class="serve_center_right mr10">
                        <p>磁盘写</p>
                        <linegraph :id="'diskWriteRate_id'" :data="diskWriteRateData" class="linegraph"></linegraph>
                    </div>
                </el-col>
            </el-row>

            <el-row class="serve_center">
                <el-col :span="12">
                    <div  class="serve_center_left rabmt10">
                        <p>Message Rate</p>
                        <linegraph :id="'messageRate_id'" :data="messageRateData" class="linegraph"></linegraph>
                    </div>
                </el-col>
                <el-col :span="12" >
                    <div class="serve_center_right mtb10 mr10">
                        <p>Message Ready Rate</p>
                        <linegraph :id="'messageReadyRate_id'" :data="messageReadyRateData" class="linegraph"></linegraph>
                    </div>
                </el-col>
            </el-row>

            <el-row class="serve_center">
                <el-col :span="12">
                    <div  class="serve_center_left">
                        <p>Message Unacknowledged Rate</p>
                        <linegraph :id="'messageUnacknowledgedRate_id'" :data="messageUnacknowledgedRateData" class="linegraph"></linegraph>
                    </div>
                </el-col>
            </el-row>
        </div>
    </div>

</template>
<script>
    import linegraph from '../network_equipment/visualNetworkEchart/MinutesCpuUtilization.vue';

    export default {
        name: 'ViewServe',
        components: {
            linegraph
        },
        data(){
            return{
                serveIp:'',
                mq_channels: 0,
                mq_connections: 0,
                mq_consumers: 0,
                mq_disk_reads: 0,
                mq_disk_writes: 0,
                mq_exchanges: 0,
                mq_messages: 0,
                mq_queues: 0,
                diskReadRateData:{
                    title:'',
                    legendData:[],
                    xAxisData:[],
                    seriesData:[],
                    animation:true
                },
                diskWriteRateData:{
                    title:'',
                    legendData:[],
                    xAxisData:[],
                    seriesData:[],
                    animation:true
                },
                messageRateData:{
                    title:'',
                    legendData:[],
                    xAxisData:[],
                    seriesData:[],
                    animation:true
                },
                messageReadyRateData:{
                    title:'',
                    legendData:[],
                    xAxisData:[],
                    seriesData:[],
                    animation:true
                },
                messageUnacknowledgedRateData:{
                    title:'',
                    legendData:[],
                    xAxisData:[],
                    seriesData:[],
                    animation:true
                },
                monitorTime:'',
                rabbitMQData:null,
                rabbitMQHost:'',

            }
        },
        computed: {
        },
        created() {
            this.monitorTime=[this.Format(new Date()-12*60*60*1000), this.Format(new Date())];
            this.queryOneRabbitMQ();
            this.timer=setInterval(()=>{ this.changeQueryHost(); },180000);
        },
        mounted() {
        },
        methods: {
            queryOneRabbitMQ(){
                this.$http.get(`monitor/api/middleware/?middleware_type=RABBITMQ&current_page=1&pre_page=1`, {
                    headers: {'token':localStorage.getItem('token')}
                }).then((res) => {
                    const oneRabbitMQData = res.data;
                    const ip=oneRabbitMQData.data[0].ip_address;
                    const port=oneRabbitMQData.data[0].port;
                    this.rabbitMQHost=port+'/'+ip;
                    this.optionData(ip,port);
                    const curTime=Date.parse(this.monitorTime[1])/1000;
                    const startTime=Date.parse(this.monitorTime[0])/1000;
                    this.query_history(startTime,curTime,ip);
                }).catch( (error)=> {
                    this.$message.error(JSON.stringify(error.response.data));
                });
            },
            queryRabbitMQ(query){
                if (query !== '') {
                    this.$http.get(`monitor/api/middleware/search?middleware_type=RABBITMQ&query=${query}`, {
                        headers: {'token':localStorage.getItem('token')}
                    }).then((res) => {
                        this.rabbitMQData = res.data;
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
                const rabbitMQ_name=this.redisHost.split('/');
                const rabbitMQ_port=rabbitMQ_name[0];
                const rabbitMQ_ip=rabbitMQ_name[1];
                this.optionData(rabbitMQ_ip,rabbitMQ_port);
                this.query_history(startTime,curTime, rabbitMQ_ip);
            },
            optionData(rabbitMQ_ip,rabbitMQ_port){
                this.$http.get(`monitor/api/middleware/monitor/?middleware_name=RABBITMQ_${rabbitMQ_ip}_${rabbitMQ_port}`, {
                    headers:{'token': this.token}
                }).then((res)=>{
                    this.serveIp=res.data.LOGIC_IP;
                    this.mq_channels=res.data.CHANNELS;
                    this.mq_consumers = res.data.CONSUMERS;
                    this.mq_disk_reads=res.data.DISK_READS;
                    this.mq_disk_writes=res.data.DISK_WRITES;
                    this.mq_exchanges=res.data.EXCHANGES;
                    this.mq_messages = res.data.MESSAGES;
                    this.mq_queues = res.data.QUEUES;

                }).catch( (error) => {
                    this.$message.error(JSON.stringify(error.response.data));
                });
            },
            query_history(startTime,curTime, ip){
                this.$http.get(`monitor/api/middleware/history/?start=`+startTime+`&end=`+curTime+`&m=sum:DISK_READS_DETAILS_RATE{logicIp=${ip}}`, {
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
                    this.diskReadRateData.xAxisData=lineXtime;
                    this.diskReadRateData.seriesData=[{
                        name: "磁盘读",
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
                }).catch( (error) => {
                    this.$message.error(JSON.stringify(error.response.data));
                });

                this.$http.get(`monitor/api/middleware/history/?start=`+startTime+`&end=`+curTime+`&m=sum:DISK_WRITES_DETAILS_RATE{logicIp=${ip}}`, {
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
                    this.diskWriteRateData.xAxisData=lineXtime;
                    this.diskWriteRateData.seriesData=[{
                        name: "磁盘写",
                        type: "line",
                        smooth: true,
                        symbol: 'circle',
                        symbolSize: 3,
                        lineStyle: {
                            normal: {
                                color:'#d14352'
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
                                    offset: 0, color: 'rgba(209,67,82, 0.9)' // 0% 处的颜色
                                }, {
                                    offset: 0.8, color: 'rgba(209,67,82, 0)' // 100% 处的颜色
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

                this.$http.get(`monitor/api/middleware/history/?start=`+startTime+`&end=`+curTime+`&m=sum:MESSAGES_DETAILS_RATE{logicIp=${ip}}`, {
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
                    this.messageRateData.xAxisData=lineXtime;
                    this.messageRateData.seriesData=[{
                        name: "Message Rate",
                        type: "line",
                        smooth: true,
                        symbol: 'circle',
                        symbolSize: 3,
                        lineStyle: {
                            normal: {
                                color:'#d19644'
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
                                    offset: 0, color: 'rgba(209,150,68, 0.9)' // 0% 处的颜色
                                }, {
                                    offset: 0.8, color: 'rgba(209,150,68, 0)' // 100% 处的颜色
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

                this.$http.get(`monitor/api/middleware/history/?start=`+startTime+`&end=`+curTime+`&m=sum:MESSAGES_READY_DETAILS_RATE{logicIp=${ip}}`, {
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
                    this.messageReadyRateData.xAxisData=lineXtime;
                    this.messageReadyRateData.seriesData=[{
                        name: "Message Ready Rate",
                        type: "line",
                        smooth: true,
                        symbol: 'circle',
                        symbolSize: 3,
                        lineStyle: {
                            normal: {
                                color:'#d16c97'
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
                                    offset: 0, color: 'rgba(209,108,51, 0.9)' // 0% 处的颜色
                                }, {
                                    offset: 0.8, color: 'rgba(209,108,51, 0)' // 100% 处的颜色
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

                this.$http.get(`monitor/api/middleware/history/?start=`+startTime+`&end=`+curTime+`&m=sum:MESSAGES_UNACKNOWLEDGED_DETAILS_RATE{logicIp=${ip}}`, {
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
                    this.messageUnacknowledgedRateData.xAxisData=lineXtime;
                    this.messageUnacknowledgedRateData.seriesData=[{
                        name: "Message Unacknowledged Rate",
                        type: "line",
                        smooth: true,
                        symbol: 'circle',
                        symbolSize: 3,
                        lineStyle: {
                            normal: {
                                color:'#a056d1'
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
                                    offset: 0, color: 'rgba(160,86,209, 0.9)' // 0% 处的颜色
                                }, {
                                    offset: 0.8, color: 'rgba(160,86,209, 0)' // 100% 处的颜色
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
    .top_font_wb{
        padding-top:3px;
    }
    dl{
        text-align: center;
      dd{
          margin-top: 2px;
      }
    }
    .linegraph{
        height: 170px;
    }
    .serve_top_left,.serve_top_char_ip{
        height:120px;
        background:#24273e;
        border-radius: 10px;
    }
    .serve_top_char{
        height:55px;
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
    .rabmt10{
         margin: 10px 10px 0 10px;
     }

    .serve_top{
        height:120px;
    }
    .serve_center,.serve_bottom{
        p{
            color:#03c2ec;
            font-size:12px;
            padding:10px 0 0 10px;
            font-weight: 600;
        }
    }
</style>