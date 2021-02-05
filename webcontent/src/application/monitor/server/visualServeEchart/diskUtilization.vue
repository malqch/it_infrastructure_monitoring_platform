<template>
    <div class="box-container">
        <div :id=id :data=charts  class="echart-container"></div>
    </div>
</template>

<script>
    require('echarts/lib/component/title');
    import 'echarts-liquidfill/src/liquidFill.js';
    export default {
        name: "diskUseEcharts",
        data(){
            return{
                charts:0.1,
                ChartLineGraph:null,
            }
        },
        //  深度监听 父组件刚开始没有值，只有图标的配置项
        //  父组件ajax请求后改变数据的值，传递过来，图标已生成，监听传过来的值的改变
        // deep:true.深度监听，确保data中子项修改也能监听到
        watch:{
            data:{
                handler(newValue) {
                    this.drawliquidFill(this.id,newValue);
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
                type: Number
            }
        },
        mounted() {
            this.drawliquidFill(this.id,this.data);
        },
        methods:{
            drawliquidFill(id,charts){
                let _this = this;
                let myChart = document.getElementById(id);
                this.diskEcharts = this.$echarts.init(myChart);
                this.optionCpu= {
                    title: {//标题
                        text:'磁盘利用率',
                        textStyle: {//标题的样式
                            color:'#0ab5e1',//字体颜色#f60
//                            color:'#fff',//字体颜色#f60
                            align: 'center',//文字的水平方式
                            verticalAlign: 'middle',//文字的垂直方式
                            fontSize:12
                        },
                        left: 'center',//定位
                        bottom:'5'
                    },
                    series: [{
                        type: 'liquidFill',//类型
                        data: [charts,charts,charts],//数据是个数组 数组的每一项的值是0-1
                        label:{
                            normal: {
                                formatter:function(param){
                                    return parseInt(param.value*100)+'%';
//                                    return (param.value)*100+'%';
                                },//水球上显示文字，可以设置任意文字
                                show: true,
                                textStyle: {
                                    fontSize: 18,
                                    color:'#fff'
                                },
                            }
                        },
                        outline: {
                            show: true , //是否显示轮廓 布尔值
                            borderDistance: 0, //外部轮廓与图表的距离 数字
                            itemStyle:{
                                borderColor:'rgba(236,57,91,0.15)', //边框的颜色
                                borderWidth: 7,  //边框的宽度
                                shadowBlur: 9 , //外部轮廓的阴影范围 一旦设置了内外都有阴影
                                shadowColor: 'rgba(236,57,91,0.15)', //外部轮廓的阴影颜色
                            }
                        },
                        backgroundStyle: {
                            //                        color:'rgba(255,0,0,0.1)',//图表的背景颜色
                            color:'rgba(236,57,91,0.35)',//图表的背景颜色
                            //                        borderWidth: '10',//图表的边框宽度
                            //                        borderColor: '#000',//图表的边框颜色
                            itemStyle: {
                                shadowBlur:100,//设置无用
                                shadowColor: '#ec395b',//设置无用f60
                                opacity: 1 //设置无用
                            }
                        },
                        itemStyle: {
                            opacity: 0.5,//波浪的透明度
                            shadowBlur: 10,//波浪的阴影范围
                            shadowColor: '#ec395b',//阴影颜色f60,
                        },
                        emphasis:{
                            itemStyle: {
                                opacity :1 //鼠标经过波浪颜色的透明度
                            }
                        },
                        color: ['rgba(236,57,91,0.7)','rgba(236,57,91,0.7)','rgba(236,57,91,0.7)',],//水波的颜色 对应的是data里面值
                        shape: 'circle',//水填充图的形状 circle默认圆形  rect圆角矩形  triangle三角形  diamond菱形  pin水滴状 arrow箭头状  还可以是svg的path
                        center: ['53%','45%'],//图表相对于盒子的位置 第一个是水平的位置 第二个是垂直的值 默认是[50%,50%]是在水平和垂直方向居中 可以设置百分比 也可以设置具体值
                        radius: '73%', //图表的大小 值是圆的直径 可以是百分比 也可以是具体值 100%则占满整个盒子 默认是40%; 百分比下是根据宽高最小的一个为参照依据
                        amplitude:5,   //振幅 是波浪的震荡幅度 可以取具体的值 也可以是百分比 百分比下是按图标的直径来算
                        waveLength:'50%',//波的长度 可以是百分比也可以是具体的像素值  百分比下是相对于直径的 取得越大波浪的起伏越小
                        phase:0 ,//波的相位弧度 默认情况下是自动
                        period: (value,index)=>{//控制波的移动速度 可以是函数 也可以是数字 两个参数  value 是data数据里面的值 index 是data值的索引

                            return index*2000;
                        },
                        direction: 'left',//波移动的速度 两个参数  left 从右往左 right 从左往右
                        waveAnimation: true, //控制波动画的开关  值是布尔值 false 是关闭动画 true 是开启动画 也是默认值
                        animationEasing: 'linear',//初始动画
                        animationEasingUpdate: 'quarticInOut',//数据更新的动画效果
                        animationDuration: 2000, //初始动画的时长，支持回调函数，可以通过每个数据返回不同的 delay 时间实现更绚丽的初始动画效果
                        animationDurationUpdate : 300 //数据更新动画的时长

                    }]
                    //backgroundColor: 'rgba(255,0,0,0.1)'容器背景颜色

                };
                this.diskEcharts.setOption(this.optionCpu);
                window.addEventListener("resize",function () {
                    _this.diskEcharts.resize();
                });
            }
        },
        beforeDestroy() {
            clearInterval(this.ChartLineGraph);
            this.ChartLineGraph = null;
        }
    }

</script>

<style lang="scss" scoped>
    .echart-container {
        height: 145px;
    }
</style>