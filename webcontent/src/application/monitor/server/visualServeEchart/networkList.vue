<template>
    <div class="box-container">
        <!--<div :id=id :data=charts  class="echart-container"></div>-->
        <div style="height:100%;width:100%">
            <div class="bodytable" :id=id><!--:style="view"-->
                    <el-row :span="24" class="list_head">
                        <el-col :span="2">名称</el-col>
                        <el-col :span="2">接收流量</el-col>
                        <el-col :span="2">发送流量</el-col>
                        <el-col :span="3">收包数</el-col>
                        <el-col :span="3">发包数</el-col>
                        <el-col :span="3">接收数据包错误总数</el-col>
                        <el-col :span="3">发送数据包错误总数</el-col>
                        <el-col :span="3">接收时丢弃数据包总数</el-col>
                        <el-col :span="3">发送时丢弃数据包总数</el-col>
                    </el-row>
                    <div class="scroll-content" id="dataWrapper">
                        <el-row :data=dutyRateData  v-for="(item,index) in this.data" :key="index" class="wrapper_div">
                            <el-col :span="2">{{item.net_name}}</el-col>
                            <el-col :span="2">{{parseInt(item.bytes_recv/1024/1024)}}</el-col>
                            <el-col :span="2">{{parseInt(item.bytes_sent/1024/1024)}}</el-col>
                            <el-col :span="3">{{item.packets_recv}}</el-col>
                            <el-col :span="3">{{item.packets_sent}}</el-col>
                            <el-col :span="3">{{parseInt(item.dropin/1024/1024)}}</el-col>
                            <el-col :span="3">{{parseInt(item.dropout/1024/1024)}}</el-col>
                            <el-col :span="3">{{parseInt(item.errin/1024/1024)}}</el-col>
                            <el-col :span="3">{{parseInt(item.errout/1024/1204)}}</el-col>
                        </el-row>
                    </div>

            </div>
        </div>
    </div>
</template>

<script>
    export default {
        name: "diskMessageList",
        data(){
            return{
                dutyRateData:[],
                ChartLineGraph:null,
            }
        },
        props:{
            id: {
                type: String,
                default: ''
            },
            data: {
                type: Array,
                default:function(){return []}
            }
        },
        computed: {
        },
        beforeDestroy() {
            clearInterval(this.ChartLineGraph);
            this.ChartLineGraph = null;
        }
    }

</script>

<style lang="scss" scoped>
    .scroll-content {
        //自定义滚动 间隔时间和方向
        position: relative;
        transition: top 0.825s; //向上移动
    }
    .bodytable {
        width: 100%;
        height: 271px;
        overflow-y: hidden;
        color:#ededed;
        font-size:12px;
        margin-top:11px;
        text-align: center;
    }
    .list_head{
        text-align: center;
        background:#22284a;
        height: 43px;
        color: #e33780;
        line-height: 43px;
    }
    .ml8{
        margin:0 8px;
    }
    .net_wid{
        width: 60px;
    }
    .net_w{
        width: 65px;
        line-height: 16px;
        margin: 7px 3px 0 4px;
    }
    .net_w2{
        line-height: 14px;
        width: 72px;
        margin:9px 7px 0px 7px;
    }
    .wrapper_div{
        margin: 10px 0px;
    }
    .table-row-odd{
        background: #31d2f5;
    }
    .table-row-even{
        background:#dfbf54;
    }

    .data-collapse {
        animation: data-col .5s;
        animation-timing-function: ease;
        animation-fill-mode: forwards;
        overflow:hidden;
    }

    @keyframes data-col {
        from {
            height: 50px;
        }
        to {
            height: 0;
        }
    }

</style>