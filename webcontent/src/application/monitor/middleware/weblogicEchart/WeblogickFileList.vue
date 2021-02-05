<template>
    <div class="box-container">
        <!--<div :id=id :data=charts  class="echart-container"></div>-->
        <div style="height:100%;width:100%">
            <div class="bodytable" :id=id :data=dutyRateData><!--:style="view"-->
                    <el-row :span="24" class="list_head">
                        <el-col :span="8">JVM线程组名</el-col>
                        <el-col :span="8">线程池更新延时</el-col>
						<el-col :span="8">线程泄露延时</el-col>
                    </el-row>
                    <div class="scroll-content" id="dataWrapper">
                        <el-row :data=dutyRateData  v-for="(item,index) in this.data" :key="index" class="wrapper_div">
                            <el-col :span="8">{{item.JVMTHREADGROUPNAMES}}</el-col>
                            <el-col :span="8">{{item.THREADPOOLRENEWALDELAYFACTOR}}</el-col>
							<el-col :span="8">{{item.LEAKSWEEPERDELAY}}</el-col>
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
//        watch:{
//            data:{
//                handler(newValue) {
//                    this.drawliquidFill(newValue);
//                },
//                deep:true
//            }
//        },
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
        margin-top:13px;
        text-align: center;
    }
    .list_head{
        text-align: center;
        background:#2c2f49;
        height: 30px;
        line-height: 30px;
        color: #e33780;
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