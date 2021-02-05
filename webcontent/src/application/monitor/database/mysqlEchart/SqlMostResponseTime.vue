<template>
    <div class="box-container">
        <div style="height:100%;width:100%">
            <div class="bodytable"  :id=id>
                <el-row :span="24" class="list_head">
                    <el-col :span="3">SCHEMA名称</el-col>
                    <el-col :span="11">SQL语句</el-col>
                    <el-col :span="3">平均等待时间</el-col>
                    <el-col :span="2">COUNT_STAR</el-col>
                    <el-col :span="2">最早执行时间</el-col>
                    <el-col :span="3">最晚执行时间</el-col>
                </el-row>
                <div class="scroll-content" :style="{top}" id="dataWrapper">
                    <el-row :data=dutyRateData  v-for="(item,index) in this.data" :key="index" class="wrapper_div">
                        <el-col :span="3">{{item.SCHEMA_NAME}}</el-col>
                        <el-col :span="11">{{item.DIGEST_TEXT}}</el-col>
                        <el-col :span="3">{{item.AVG_TIMER_WAIT}}</el-col>
                        <el-col :span="2">{{item.COUNT_STAR}}</el-col>
                        <el-col :span="2">{{item.FIRST_SEEN}}</el-col>
                        <el-col :span="3">{{item.LAST_SEEN}}</el-col>
                    </el-row>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    require('echarts/lib/component/title');
    export default {
        name: "diskMessageList",
        data(){
            return{
                dutyRateData:[],
                activeIndex: 0,
                rownumber:8,
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
                default:function () { return [] }
            },
            moveDistance:{//移动距离
                type:Number,
                default:25
            }
        },
        computed: {
            top(){
                return -this.activeIndex * 35 + "px"; //定义移动的单元高度
            }
        },
        beforeDestroy() {
            clearInterval(this.ChartLineGraph);
            this.ChartLineGraph = null;
        }
    }

</script>

<style lang="scss" scoped>
    .scroll-content {
        /*position: relative;*/
        /*transition: top 0.825s; */
        overflow: auto;
        // height: 300px;
        scrollbar-width:none; /* Firefox */
        -ms-overflow-style: none; /* IE 10+ */
    }
    ::-webkit-scrollbar {
        display: none; /* Chrome Safari */
    }
    .bodytable {
        width: 100%;
        // height: 330px;
        overflow: hidden;
        color:#fff;
        font-size:12px;
        margin-top:13px;
        text-align: center;
    }
    .list_head{
        text-align: center;
        background:#2c2f49;
        height: 30px;
        line-height: 30px;
        color:#b08ff9;
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
    .wrapper_div{
        margin:16px 0;
    }

</style>