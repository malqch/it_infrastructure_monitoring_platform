<template>
    <div>
        <div class="wrapper" v-if="remain_alarm_count[0] && total_alarm_count[0]">
            <el-row :span="24" class="mlr10 mt10">
                <el-col :span="12">
                    <div class="serve_top_r_t asset_center_height mr10">
                        <p>告警中数量/告警总数量</p>
                        <p style="padding-top: 50px; text-align: center; font-size: 80px">{{remain_alarm_count[0].value}}/{{total_alarm_count[0].value}}</p>
                    </div>
                </el-col>
                <el-col :span="12">
                    <div class="serve_top_r_t asset_center_height">
                        <p>告警信息</p>
                        <div>
                            <el-col :span="9">
                                <ul class="warnNum">
                                    <li><span class="warn_word">提示</span><span class="warn_num">{{hintNum}}</span></li>
                                    <li><span class="warn_word">报警</span><span class="warn_num">{{reportNum}}</span></li>
                                    <li><span class="warn_word">重要</span><span class="warn_num">{{importNum}}</span></li>
                                    <li><span class="warn_word">严重</span><span class="warn_num">{{badlyNum}}</span></li>
                                    <li><span class="warn_word">紧急</span><span class="warn_num">{{urgencyNum}}</span></li>
                                </ul>
                            </el-col>
                            <el-col :span="13" :offset="1">
                                <div class="warnDiv">
                                    <ul>
                                        <li v-for="(item,index) in warnData" :key="index" :class="item.iconClass">
                                            <div>{{item.info}}</div>
                                            <div class="warn_time_p">{{item.time}}</div>
                                        </li>
                                    </ul>
                                </div>
                            </el-col>
                        </div>
                    </div>
                </el-col>
            </el-row>
            <el-row class="mtb10">
                <el-col :span="12">
                    <div class="serve_top_r_t asset_center_height mlr10">
                        <p>5分钟内cpu利用率TOP3</p>
                        <topnBar :id="'cpuTop'" :data="cpuTopData"></topnBar>
                    </div>
                </el-col>
                <el-col :span="12">
                    <div class="serve_top_r_t asset_center_height mr10">
                        <p>5分钟内内存利用率TOP3</p>
                        <topnBar :id="'memTop'" :data="memTopData"></topnBar>
                    </div>
                </el-col>
            </el-row>
            <el-row>
                <el-col :span="12">
                    <div class="serve_top_r_t asset_center_height mlr10">
                        <p>不同等级告警数量统计饼图</p>
                        <LevelCountAlarm :id="level_id" :data="level_alarm_count"></LevelCountAlarm>
                    </div>
                </el-col>
                <el-col :span="12">
                    <!-- <div class="serve_top_r_t asset_center_height mr10">
                         <p>不同等级告警数量统计柱状图</p>
                         <TotalCountAlarm2 :id="level_id_1" :data="level_alarm_count1"></TotalCountAlarm2>
                     </div>-->
                    <div class="serve_top_r_t asset_center_height mb10 mr10">
                        <p>不同类型告警数量统计柱状图</p>
                        <TotalCountAlarm1 :id="type_id_1" :data="type_alarm_count1"></TotalCountAlarm1>
                    </div>
                </el-col>
            </el-row>
            <el-row>
                <el-col :span="12">
                    <div class="serve_top_r_t asset_center_height mb10 mlr10">
                        <p>不同标签告警数量统计柱状图</p>
                        <TagCountAlarm :id="tag_id" :data="tag_alarm_count"></TagCountAlarm>
                    </div>
                </el-col>
                <el-col :span="12">
                    <div class="serve_top_r_t asset_center_height mr10">
                        <p>不同业务告警数量统计柱状图</p>
                        <BusinessCountAlarm :id="business_id" :data="business_alarm_count"></BusinessCountAlarm>
                    </div>
                </el-col>
            </el-row>
        </div>
    </div>
</template>
<script>
    import LevelCountAlarm from "./alarm/LevelCountAlarm";
    // import ServerTypeCountAlarm from './alarm/ServerTypeCountAlarm';
    import TotalCountAlarm1 from "./alarm/TotalCountAlarm1";
    // import TotalCountAlarm2 from "./alarm/TotalCountAlarm2";
    import TagCountAlarm from "./alarm/TagCountAlarm";
    import BusinessCountAlarm from "./alarm/BusinessCountAlarm";
    import topnBar from "./alarm/topnBar.vue";
    // import Business from "../echart/right/rightBotChart";
    export default {
        name: 'ViewServe',
        components: {
            // Business,
            TotalCountAlarm1,
            // TotalCountAlarm2,
            // ServerTypeCountAlarm,
            LevelCountAlarm,
            topnBar,
            TagCountAlarm,
            BusinessCountAlarm
        },
        data(){
            return{
                level_alarm_count: [],
                type_alarm_count: [],
                total_alarm_count: [],
                remain_alarm_count: [],
                level_alarm_count1: [],
                type_alarm_count1: [],
                tag_alarm_count: [],
                business_alarm_count: [],
                total_id: 'total_id',
                level_id: 'level_id',
                level_id_1: 'level_id_1',
                type_id: 'type_id',
                type_id_1: 'type_id_1',
                tag_id: 'tag_id',
                business_id: 'business_id',
                cpuTopData:{
                    myColor:[],
                    yAxisData : [],
                    seriesData : []
                },
                memTopData:{
                    myColor:[],
                    yAxisData : [],
                    seriesData : []
                },
                warnData:[],
                hintNum:0,
                reportNum:0,
                badlyNum:0,
                importNum:0,
                urgencyNum:0            }
        },
        computed: {
        },
        created() {
            this.optionData();
            this.queryTopn();
        },
        methods: {
            optionData(){
                this.$http.get(`monitor/api/alarm_detail/alarm_count/`, {
                    headers:{
                        'token': localStorage.getItem('token')
                    }
                }).then((res)=>{
                    //console.log(res.data);
                    res.data.level_count.map( item=>{
                        if(item.name=='5'){
                            this.urgencyNum=item.value;
                            console.log(this.urgencyNum);
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
                    // 不同等级饼图数据
                    this.level_alarm_count = res.data['level_count'];
                    for (let i in this.level_alarm_count) {
                        if (this.level_alarm_count[i].name == 1) {
                            this.level_alarm_count[i].name = '提示'
                        } else if (this.level_alarm_count[i].name == 2) {
                            this.level_alarm_count[i].name = '报警'
                        } else if (this.level_alarm_count[i].name == 3) {
                            this.level_alarm_count[i].name = '重要'
                        } else if (this.level_alarm_count[i].name == 4) {
                            this.level_alarm_count[i].name = '严重'
                        } else if (this.level_alarm_count[i].name == 5) {
                            this.level_alarm_count[i].name = '紧急'
                        } else {
                            this.level_alarm_count[i].name = ''
                        }}
                    const level_xData=[];
                    const level_yData=[];
                    for(let item of this.level_alarm_count){
                        level_xData.push(item.name);
                        level_yData.push(item.value);
                    }
                    // 不同等级柱状图数据
                    this.level_alarm_count1={
                        xData:level_xData,
                        yData:level_yData
                    };
                    // 不同类型饼图数据
                    this.type_alarm_count = res.data['object_count'];
                    const type_xData=[];
                    const type_yData=[];
                    for(let item of this.type_alarm_count){
                        type_xData.push(item.name);
                        type_yData.push(item.value);
                    }
                    // 不同类型柱状图数据
                    this.type_alarm_count1={
                        xData:type_xData,
                        yData:type_yData
                    };
                    // 标签柱状图数据
                    const tag_xData=[];
                    const tag_yData=[];
                    for(let item of res.data['tag_count']){
                        tag_xData.push(item.name);
                        tag_yData.push(item.value);
                    }
                    this.tag_alarm_count={
                        xData:tag_xData,
                        yData:tag_yData
                    };
                    // 业务柱状图数据
                    const business_xData=[];
                    const business_yData=[];
                    for(let item of res.data['business_count']){
                        business_xData.push(item.name);
                        business_yData.push(item.value);
                    }
                    this.business_alarm_count={
                        xData:business_xData,
                        yData:business_yData
                    };
                    this.total_alarm_count = res.data['total_count'];
                    this.remain_alarm_count = res.data['remain_count'];

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
                }).catch( (error) => {
                    this.$message.error(JSON.stringify(error.response.data));
                });
            },
            queryTopn(){
                this.$http.get(`monitor/api/analysis/?type=cpu_percent&num=3`, {
                    headers:
                        {
                            'token':localStorage.getItem('token')
                        }
                }).then((res) => {
                    if(res.data.length!=0 || res.data!=null){
                        const ip_name=res.data.map( item =>{ return item.host_name+'/'+item.host_ip});
                        const indicator_value=res.data.map( item =>{ return item.indicator_value});
                        this.cpuTopData.myColor=['#d0a00e', '#34da62', '#00e9db'];
                        this.cpuTopData.yAxisData=ip_name;
                        this.cpuTopData.seriesData=indicator_value;
                    }
                }).catch( (error)=> {
                    this.$message.error(JSON.stringify(error.response.data));
                });
                this.$http.get(`monitor/api/analysis/?type=mem_percent&num=3`, {
                    headers:
                        {
                            'token':localStorage.getItem('token')
                        }
                }).then((res) => {
                    if(res.data.length!=0 || res.data!=null){
                        const ip_name=res.data.map( item =>{ return item.host_name+'/'+item.host_ip});
                        const indicator_value=res.data.map( item =>{ return item.indicator_value});
                        this.memTopData.myColor=['#0096f3', '#33CCFF', '#33FFCC'];
                        this.memTopData.yAxisData=ip_name;
                        this.memTopData.seriesData=indicator_value;
                    }
                }).catch( (error)=> {
                    this.$message.error(JSON.stringify(error.response.data));
                });
            }
        },
        beforeDestroy() {
            if (this.timer) {
                clearInterval(this.timer);
            }
        }
    }
</script>

<style lang="scss" scoped>
    @import "../../assets/css/fonts/font.css";
    @import "../../assets/scss/echarts";
    .warn_word{
        width:60px;
        display: inline-block;
        text-align: center;
    }
    .warnDiv{
        overflow: auto;
        height: 218px;
        color: #a165cc;
        font-size: 12px;
        scrollbar-width:none; /* Firefox */
        -ms-overflow-style: none; /* IE 10+ */
        li{
            list-style: none;
            margin-left: 30px;
            letter-spacing: 1px;
        }

    }
    .warnNum{
        list-style: none;
        margin-left: 60px;
        margin-top: 16px;
        margin-right:15px;
        border-right:1px dashed #4e5353;
        li{
            line-height: 35px;
            color:#ccc;
            font-size: 14px;
            text-align: center;
        }
        .warn_num{
            width: 60px;
            display: inline-block;
            text-align: center;
            font-size: 18px;
            color:#f7d630
        }
    }
    .warn_icon{
        &:before{
            width: 18px;
            height: 18px;
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
            width: 18px;
            height: 18px;
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
            width: 18px;
            height: 18px;
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
            width: 18px;
            height: 18px;
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
            width: 18px;
            height: 18px;
            content: '';
            background: url('../../assets/img/index/urgency.png')no-repeat left;
            background-size: 100%;
            display: inline-block;
            position: relative;
            left: -30px;
            top: 23px;
        }
    }
    ::-webkit-scrollbar {
        display: none; /* Chrome Safari */
    }
    .wrapper{
        background: #191a2c;
    }
    .serve_bottom{
        margin:13px 0;
    }
    .serve_center,.serve_bottom{
        p{
            color:#03c2ec;
            font-size:12px;
            padding:10px 0 0 10px;
            font-weight: 600;
        }
    }
    .serve_center_left,.serve_center_right{
        height:200px;
        background:#24273e;
        border-radius: 10px;
    }
    .serve_center_left{
        margin:0 13px 0 20px;
    }
    dl{
        dt{
            color:#e5bb2e;
            display: inline;
        }
        .time{
            font-family:"DS-DIGI";
            font-size:26px;
        }
        .serve_name{
            font-size:16px;
        }
        dd{
            color:#fff;
            font-size:12px;
            margin-top:3px;
        }
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
    .serve_bottom_left,.serve_bottom_right{
        height:390px;
        background:#24273e;
        border-radius: 10px;
    }
    .serve_bottom_left{
        margin:0 10px;
    }
    .asset_center_height{
        height:265px;
    }
    .serve_bottom,.serve_bottom_left{
        p{
            color:#03c2ec;
            font-size:12px;
            padding:10px 0 0 10px;
            font-weight: 600;
        }
    }
    .top_font{
        text-align: center;
        padding-top: 10px;
    }
    .serve_top_char{
        height:70px;
        background:#24273e;
        border-radius: 10px;
    }
    .m10{
        margin:10px 0;
    }
</style>


