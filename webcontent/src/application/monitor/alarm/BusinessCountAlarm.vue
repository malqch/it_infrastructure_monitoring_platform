<template>
    <div class="box-container">
        <div :id=id :data=charts  class="echart-container"></div>
    </div>
</template>

<script>
    require('echarts/lib/component/title');
    export default {
        name: "BusinessCountAlarm",
        data(){
            return{
                charts: null,
                ChartLineGraph:null,
            }
        },
        props:{
            id: {
                type: String,
                default: ''
            },
            data: {
                type: Object,
                default:null
            }
        },
        computed: {
        },
        watch:{
            data:{
                handler(newValue) {
                    this.drawLineGraph(this.id,newValue);
                },
                deep:true
            }

        },
        mounted() {
            if (this.data != null) {
                this.drawLineGraph(this.id, this.data);
            }
        },
        methods:{
            drawLineGraph(id,charts){
                let _this = this;
                let myChart = document.getElementById(id);
                this.ChartLineGraph = this.$echarts.init(myChart);
                this.option = {
                    tooltip: {
                        trigger: 'axis',
                        axisPointer: { // 坐标轴指示器，坐标轴触发有效
                            type: 'shadow' // 默认为直线，可选为：'line' | 'shadow'
                        }
                    },
                    grid: {
                        left: '2%',
                        right: '3%',
                        bottom: '14%',
                        top:'16%',
                        containLabel: true
                    },
                    legend: {
                        data: ['数量'],
                        right: 10,
                        top:8,
                        textStyle: {
                            color: "#fff"
                        },
                        itemWidth: 12,
                        itemHeight: 10,
                        // itemGap: 35
                    },
                    xAxis: {
                        type: 'category',
                        data:charts.xData,
                        axisLine: {
                            lineStyle: {
                                color: 'white'
                            }
                        },
                        axisLabel: {
                            interval:0,
                            // rotate: 40,
                            textStyle: {
                                fontFamily: 'Microsoft YaHei'
                            }
                        },
                    },

                    yAxis: {
                        type: 'value',
//                        max:'1200',
                        axisLine: {
                            show: false,
                            lineStyle: {
                                color: 'white'
                            }
                        },
                        splitLine: {
                            show: true,
                            lineStyle: {
                                color: 'rgba(255,255,255,0.3)'
                            }
                        },
                        axisLabel: {}
                    },
                    dataZoom: [{
                        "show": true,
                        "height": 12,
                        "xAxisIndex": [
                            0
                        ],
                        bottom:'8%',
                        start: 0,
                        end: 100,
                        handleSize: '110%',
                        handleStyle:{color:"#d3dee5"},
                        textStyle:{color:"#fff"},
                        borderColor:"#90979c"
                    }, {
                        "type": "inside",
                        "show": true,
                        "height": 15,
                        "start": 1,
                        "end": 35
                    }],
                    series: [{
                        name: '数量',
                        type: 'bar',
                        barWidth: '15%',
                        itemStyle: {
                            normal: {
                                color: new this.$echarts.graphic.LinearGradient(0, 0, 0, 1, [{
                                    offset: 0,
                                    color: '#8bd46e'
                                }, {
                                    offset: 1,
                                    color: '#09bcb7'
                                }]),
                                barBorderRadius: 11,
                            }

                        },
                        data:charts.yData
                    }]
                };
                this.ChartLineGraph.setOption(this.option);
                /*window.addEventListener("resize",function () {
                    _this.ChartLineGraph.resize();
                })*/
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
        height: 240px;
    }

</style>