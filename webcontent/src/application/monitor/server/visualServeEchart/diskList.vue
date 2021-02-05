<template>
    <div class="box-container">
        <!--<div :id=id :data=charts  class="echart-container"></div>-->
        <div style="height:100%;width:100%">
            <div class="bodytable"  :id=id><!--:style="view" :data=dutyRateData-->
                    <el-row :span="24" class="list_head">
                        <el-col :span="4">名称</el-col>
                        <el-col :span="3">文件系统</el-col>
                        <el-col :span="3">挂载点</el-col>
                        <el-col :span="4">磁盘可用</el-col>
                        <el-col :span="3">磁盘总量</el-col>
                        <el-col :span="4">磁盘使用</el-col>
                        <el-col :span="3">磁盘利用率</el-col>
                    </el-row>
                <!--:style="{height:height*lineNum + 'px'}"-->
                   <div  class="rollScreen_container" id ="rollScreen_container" :class="{anim:animate==true}">
                      <el-row :data=dutyRateData  v-for="(item,index) in this.data" :key="index" class="wrapper_div rollScreen_list" :style = {transform:transform} :class="{rollScreen_list_unanim:num===0}">
                          <el-col :span="4">{{item.disk_name}}</el-col>
                          <el-col :span="3">{{item.fstype}}</el-col>
                          <el-col :span="3">{{item.mountpoint}}</el-col>
                          <el-col :span="4">{{parseInt(item.disk_free/1024/1024)}}MB</el-col>
                          <el-col :span="3">{{parseInt(item.disk_total/1024/1024)}}MB</el-col>
                          <el-col :span="4">{{parseInt(item.disk_used/1024/1024)}}MB</el-col>
                          <el-col :span="3">{{parseInt(item.disk_percent)}}%</el-col>
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
                num: 0,
                animate:false,

            }
        },
        //  深度监听 父组件刚开始没有值，只有图标的配置项
        //  父组件ajax请求后改变数据的值，传递过来，图标已生成，监听传过来的值的改变
        // deep:true.深度监听，确保data中子项修改也能监听到
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
                default:()=>{
                    return [];
                }
            },
            height: {
                default: 40,
                type: Number
            },
            lineNum: {
                default: 5,
                type: Number
            }
        },
        computed: {
            top(){
//                return -this.activeIndex * this.moveDistance + "px"; //定义移动的单元高度
                return -this.activeIndex * 35 + "px"; //定义移动的单元高度
            },
            transform: function () {
                return 'translateY(-' + this.num * this.height + 'px)'
            }

        },
        mounted() {
            this.drawliquidFill(this.data);
        },
        created(){
//            this.drawliquidFill(this.data);
//            setInterval(this.scroll(this.data),3000)
//            this.scroll(this.data)
        },
        methods:{
            drawliquidFill(){//dutyRateData
                /*setInterval(function () {
                    if (_this.num !== dutyRateData.length) {
                        _this.num++
                    } else {
                        _this.num = 0
                    }
                }, 3000)*/
                /*this.animate=true;    // 因为在消息向上滚动的时候需要添加css3过渡动画，所以这里需要设置true
            setTimeout(()=>{
                    dutyRateData.push(dutyRateData[0]);
                    dutyRateData.shift();
                    this.animate=false;  // margin-top 为0 的时候取消过渡动画，实现无缝滚动
                },5000)*/

                /*window.addEventListener("resize",function () {
                    _this.diskEcharts.resize();
                });*/
            },
            /*scroll(dutyRateData){
                this.animate=true;    // 因为在消息向上滚动的时候需要添加css3过渡动画，所以这里需要设置true

                /!*setTimeout(()=>{
                    dutyRateData.push(dutyRateData[0]);  // 将数组的第一个元素添加到数组的
                    dutyRateData.shift();               //删除数组的第一个元素
                    this.animate=false;  // margin-top 为0 的时候取消过渡动画，实现无缝滚动
                },5000)*!/
            }*/
        },
        beforeDestroy() {
            clearInterval(this.ChartLineGraph);
            this.ChartLineGraph = null;
        }
    }

</script>

<style lang="scss" scoped>
    .rollScreen_container{
        position:relative;
        /*overflow: hidden;*/
        color: #ededed;
        overflow: auto;
        height: 233px;
        scrollbar-width:none; /* Firefox */
        -ms-overflow-style: none; /* IE 10+ */
    }
    .rollScreen_list{
        transition: 1s linear;
    }
    .rollScreen_list_unanim{
        transition: none
    }


    .anim{
        transition: all 0.5s;
        margin-top: -30px;
    }



    .wrapper_div{
        margin: 15px 0;
    }
    .bodytable {
        width: 100%;
        height: 271px;
        /*overflow-y: hidden;*/
        font-size:12px;
        text-align: center;

    }
    ::-webkit-scrollbar {
        display: none; /* Chrome Safari */
    }
    .list_head{
        text-align: center;
        background:#22284a;
        height: 30px;
        line-height: 30px;
        color:#b08ff9;
        margin-top: 10px;
    }

</style>