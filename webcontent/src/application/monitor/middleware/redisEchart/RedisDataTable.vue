<template>
    <div class="box-container">
        <div :id=id :data=charts  class="echart-container"></div>
    </div>
</template>

<script>
//    let echarts = require("echarts");
//    import echarts from 'echarts'
//    require("echarts/lib/chart/effectScatter");

    export default {
        name: "memWater",
        data(){
            return{
                charts:0.1,
                datalist:[],
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
                type: Array,
                default:function(){return []}
            }
        },
        mounted() {
            if(this.data!=null){
                this.drawliquidFill(this.id,this.data);
            }
        },
        methods:{
            drawliquidFill(id,charts){
                const datas=[];
                this.datalist = [{
                    offset: [50, 50],
                    symbolSize: 80,
                    opacity: .95,
                    color: new this.$echarts.graphic.LinearGradient(0, 0, 0, 1, [{
                        offset: 0,
                        color: '#29c0fb'
                    }, {
                        offset: 1,
                        color: '#2dc5b9'
                    }]),
                }, {
                    offset: [30, 75],
                    symbolSize: 72,
                    opacity: .95,
                    color: new this.$echarts.graphic.LinearGradient(0, 0, 0, 1, [{
                        offset: 0,
                        color: '#35d17e'
                    }, {
                        offset: 1,
                        color: '#49ddb2'
                    }]),
                }, {
                    offset: [10, 28],
                    symbolSize: 70,
                    opacity: .95,
                    color: new this.$echarts.graphic.LinearGradient(0, 0, 0, 1, [{
                        offset: 0,
                        color: '#e5d273'
                    }, {
                        offset: 1,
                        color: '#e4a37f'
                    }]),
                }, {
                    offset: [29, 18],
                    symbolSize: 65,
                    opacity: .95,
                    color: new this.$echarts.graphic.LinearGradient(0, 0, 0, 1, [{
                        offset: 0,
                        color: '#277aec'
                    }, {
                        offset: 1,
                        color: '#57c5ec'
                    }]),
                }, {
                    offset: [80, 58],
                    symbolSize: 60,
                    opacity: .95,
                    color: new this.$echarts.graphic.LinearGradient(0, 0, 0, 1, [{
                        offset: 0,
                        color: '#e54948'
                    }, {
                        offset: 1,
                        color: '#f08456'
                    }]),
                }, {
                    offset: [66, 24],
                    symbolSize: 58,
                    opacity: .7,
                    color: new this.$echarts.graphic.LinearGradient(0, 0, 0, 1, [{
                        offset: 0,
                        color: '#11c46e'
                    }, {
                        offset: 1,
                        color: '#f08456'
                    }]),
                }, {
                    offset: [65, 90],
                    symbolSize: 45,
                    opacity: .68,
                    color: new this.$echarts.graphic.LinearGradient(0, 0, 0, 1, [{
                        offset: 0,
                        color: '#ff4141'
                    }, {
                        offset: 1,
                        color: '#ff8989'
                    }]),
                }];
                for (let i = 0; i < charts.length; i++) {
                    const item = charts[i];
                    const itemToStyle = this.datalist[i];
                    datas.push({
                        name: item.name + '\n' + item.value,
                        value: itemToStyle.offset,
                        symbolSize: itemToStyle.symbolSize,
                        label: {
                            normal: {
                                textStyle: {
                                    fontSize: 12,
                                    fontWeight:800,
                                    lineHeight: 22,
                                }
                            }
                        },
                        itemStyle: {
                            normal: {
                                color: itemToStyle.color,
                                opacity: itemToStyle.opacity
                            }
                        },
                    })
                }

                let myChart = document.getElementById(id);
                let monEchart = this.$echarts.init(myChart);
                this.option = {
                    grid: {
                        show: false,
                        top: 30,
                        bottom: 30,
                        right:10
                    },
                    xAxis: [{
                        gridIndex: 0,
                        type: 'value',
                        show: false,
                        min: 0,
                        max: 100,
                        nameLocation: 'middle',
                        nameGap: 5
                    }],
                    yAxis: [{
                        gridIndex: 0,
                        min: 0,
                        show: false,
                        max: 100,
                        nameLocation: 'middle',
                        nameGap: 30
                    }],
                    series: [{
                        type: 'effectScatter',
                        hoverAnimation: true,
                        label: {
                            normal: {
                                show: true,
                                formatter: '{b}',
                                color: '#fff',
                                textStyle: {
                                    fontSize: '12'
                                }
                            },
                        },
                        itemStyle: {
                            normal: {
                                color: '#00acea'
                            }
                        },
                        data: datas
                    }]
                };
                monEchart.setOption(this.option);
                setTimeout(function() {
                    window.onresize = ()=> {
                        monEchart.resize();
                    }
                }, 200)
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
        height: 245px;
    }
</style>