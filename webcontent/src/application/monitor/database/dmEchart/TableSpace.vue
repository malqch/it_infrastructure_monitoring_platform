<template>
    <div class="box-container">
        <div style="height:100%;width:100%">
            <div class="bodytable"  :id=id>
                <el-row :span="24" class="list_head">
                    <el-col :span="6">表空间名称</el-col>
                    <el-col :span="6">空闲表空间</el-col>
                    <el-col :span="6">表空间总大小</el-col>
                    <el-col :span="6">剩余比例</el-col>
                </el-row>
                <div class="scroll-content rollScreen_container" :style="{top}" id="dataWrapper">
                    <el-row :data=tabelSpaceData  v-for="(item,index) in this.data" :key="index" class="wrapper_div">
                        <el-col :span="6">{{item.TABLESPACE_NAME}}</el-col>
                        <el-col :span="6">{{item.FREE_SPACE}}</el-col>
                        <el-col :span="6">{{item.TOTAL_SPACE}}</el-col>
                        <el-col :span="6">{{item.FREE}}%</el-col>
                    </el-row>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    require('echarts/lib/component/title');
    export default {
        name: "tableSpaceList",
        data(){
            return{
                tabelSpaceData:[],
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
        //自定义滚动 间隔时间和方向
        position: relative;
        transition: top 0.825s; //向上移动
        /deep/ .el-row{
            line-height: 35px;
        }
    }
    ::-webkit-scrollbar {
        display: none; /* Chrome Safari */
    }
    .bodytable {
        width: 100%;
        height: 271px;
        overflow-y: hidden;
        color:#ededed;
        font-size:12px;
        margin-top:13px;
        text-align: center;
    }
    .rollScreen_container{
        position:relative;
        color: #ededed;
        overflow: auto;
        height: 233px;
        scrollbar-width:none; /* Firefox */
        -ms-overflow-style: none; /* IE 10+ */
    }
    .list_head{
        text-align: center;
        background: #2c2f49;
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


</style>