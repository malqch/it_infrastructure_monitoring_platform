<template>
    <div class="box-container">
        <div style="height:100%;width:100%">
            <div class="bodytable"  :id='id'>
                <el-row :span="24" class="list_head">
                    <el-col :span="10">SCHEMA名称</el-col>
                    <el-col :span="7">数据大小</el-col>
                    <el-col :span="7">索引大小</el-col>
                </el-row>
                <div class="scroll-content" :style="{top}" id="dataWrapper">
                    <el-row :data=sqlDiskUsage  v-for="(item,index) in this.data" :key="index" class="wrapper_div">
                        <el-col :span="10">{{item.TABLE_SCHEMA}}</el-col>
                        <el-col :span="7">{{item.data_size}}</el-col>
                        <el-col :span="7">{{item.index_size}}</el-col>
                    </el-row>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    require('echarts/lib/component/title');
    export default {
        name: "sqlDiskUsageList",
        data(){
            return{
                sqlDiskUsage:[],
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
        overflow: auto;
        height: 271px;
        scrollbar-width:none; /* Firefox */
        -ms-overflow-style: none; /* IE 10+ */
    }
    ::-webkit-scrollbar {
        display: none; /* Chrome Safari */
    }
    .bodytable {
        width: 100%;
        height: 271px;
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