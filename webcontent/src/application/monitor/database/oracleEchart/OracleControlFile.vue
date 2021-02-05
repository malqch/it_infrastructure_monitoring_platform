<template>
    <div class="box-container">
        <div style="height:100%;width:100%">
            <div class="bodytable"  :id=id>
                <el-row :span="24" class="list_head">
                    <el-col :span="4" :offset="1">名称</el-col>
                    <el-col :span="10">BLOCK_SIZE</el-col>
                    <el-col :span="4">FILE_SIZE_BLKS</el-col>
                    <el-col :span="2">IS_RECOVERY_DEST_FILE</el-col>
                </el-row>
                <div class="scroll-content" :style="{top}" id="dataWrapper">
                    <el-row :data=oracleControlFileData  v-for="(item,index) in this.data" :key="index" class="wrapper_div">
                        <el-col :span="4" :offset="1">{{item.NAME}}</el-col>
                        <el-col :span="10">{{item.BLOCK_SIZE}}</el-col>
                        <el-col :span="4">{{item.FILE_SIZE_BLKS}}</el-col>
                        <el-col :span="4">{{item.IS_RECOVERY_DEST_FILE}}</el-col>
                    </el-row>
                </div>

            </div>
        </div>
    </div>
</template>

<script>
    require('echarts/lib/component/title');
    export default {
        name: "oracleControlFileList",
        data(){
            return{
                oracleControlFileData:[],
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

            moveDistance:{
                type:Number,
                default:25
            }
        },
        computed: {
            top(){
                return -this.activeIndex * 35 + "px";
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
        /*position: relative;
        transition: top 0.825s;*/
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
        height: 270px;
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
        margin:18px 0;
    }
</style>