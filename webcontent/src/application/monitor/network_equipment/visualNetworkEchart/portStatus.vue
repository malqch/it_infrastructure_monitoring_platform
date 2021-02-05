<template>
    <div class="box-container">
        <div style="height:100%;width:100%">
            <div class="bodytable" :id=id :data=dutyRateData>
                        <el-row :span="24" class="list_head">
                        <el-col :span="16">端口名称</el-col>
                        <el-col :span="7">端口状态</el-col>
                    </el-row>
                    <div class="scroll-content" id="dataWrapper">
                        <el-row :data=dutyRateData  v-for="(item,index) in this.data" :key="index" class="wrapper_div">
                            <el-col :span="16">{{item.name}}</el-col>
                            <el-col :span="7">{{item.value==1 ? 'up' :'down'}}</el-col>
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
        watch:{
            data:{
                handler(newValue) {
                    this.drawliquidFill(newValue);
                },
                deep:true
            }
        },
        props:{
            id: {
                type: String,
                default: ''
            },
            data: {
                type: Array,
                default:function () {
                    return [];
                }
            }
        },
        mounted() {
            this.drawliquidFill(this.data);
        },
        methods:{
            drawliquidFill(dutyRateData){
                //console.log(dutyRateData);
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
       /* position: relative;
        transition: top 0.825s;*/
        overflow: auto;
        height: 272px;
        scrollbar-width:none; /* Firefox */
        -ms-overflow-style: none; /* IE 10+ */
    }
    ::-webkit-scrollbar {
        /*display: none; /* Chrome Safari */
		width: 5px;
		height: 6px;
		background: #191b2a;
    }
	::-webkit-scrollbar-thumb{
		background-color: #596077;
		border-radius: 2px;
	}
    .bodytable {
        width: 100%;
        height: 302px;
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
    .wrapper_div{
        margin:13px 0;
    }
    .data-collapse {
        animation: data-col .5s;
        animation-timing-function: ease;
        animation-fill-mode: forwards;
        overflow:hidden;
    }


</style>
