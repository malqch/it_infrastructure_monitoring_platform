<template>
    <div class="box-container">
        <div style="height:100%;width:100%">
            <div class="bodytable"  :id=id>
                <el-row :span="24" class="list_head">
                    <el-col :span="2">SCHEMA名称</el-col>
                    <el-col :span="10">SQL语句</el-col>
                    <el-col :span="2">COUNT_STAR</el-col>
                    <el-col :span="2">最早执行时间</el-col>
                    <el-col :span="2">最晚执行时间</el-col>
                </el-row>
                <div class="scroll-content" :style="{top}" id="dataWrapper">
                    <el-row :data=dutyRateData  v-for="(item,index) in this.data" :key="index" class="wrapper_div">
                        <el-col :span="2">{{item.SCHEMA_NAME}}</el-col>
                        <el-col :span="10">{{item.DIGEST_TEXT}}</el-col>
                        <el-col :span="2">{{item.COUNT_STAR}}</el-col>
                        <el-col :span="2">{{item.FIRST_SEEN}}</el-col>
                        <el-col :span="2">{{item.LAST_SEEN}}</el-col>
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
        methods:{
            drawliquidFill(dutyRateData){
                let _this = this;
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
        //自定义滚动 间隔时间和方向
        position: relative;
        transition: top 0.825s; //向上移动
        /deep/ .el-row{
            line-height: 35px;
        }
    }
    .bodytable {
        width: 100%;
        height: 271px;
        overflow-y: hidden;
        color:#fff;
        font-size:12px;
        margin:13px 10px 0 10px;
        text-align: center;
    }
    .list_head{
        text-align: center;
        background:#22284a;
        height: 30px;
        line-height: 30px;
        border-radius: 5px;
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

    @keyframes data-col {
        from {
            height: 50px;
        }
        to {
            height: 0;
        }
    }

</style>