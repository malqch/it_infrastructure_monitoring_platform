<template>
    <div class="box-container">
        <div style="height:100%;width:100%">
            <div class="bodytable"  :id=id>
                <el-row :span="24" class="list_head">
                    <el-col :span="4">SESS_ID</el-col>
                    <el-col :span="12">SQL_TEXT</el-col>
                    <el-col :span="4">SQL_ID</el-col>
                    <el-col :span="4">运行时间</el-col>
                </el-row>
                <div class="scroll-content"  id="dataWrapper">
                    <el-row :data=dmLongExecSqlData  v-for="(item,index) in this.data" :key="index" class="wrapper_div">
                        <el-col :span="4">{{item.SESS_ID}}</el-col>
                        <el-col :span="12">{{item.SQL_TEXT}}</el-col>
                        <el-col :span="4">{{item.SQL_ID}}</el-col>
                        <el-col :span="4">{{item.EXEC_TIME}}</el-col>
                    </el-row>
                </div>

            </div>
        </div>
    </div>
</template>

<script>
    require('echarts/lib/component/title');
    export default {
        name: "dmLongExecSqlList",
        data(){
            return{
                dmLongExecSqlData:[],
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
        position: relative;
        transition: top 0.825s;
    }
    .bodytable {
        width: 100%;
        height: 271px;
        overflow-y: hidden;
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
        margin:18px 0;
    }

</style>