<template>
    <div :id="id" ref="charts" class="echart_container"></div>
</template>

<script>
    export default{
        name:'lineCharts',
        props:{
            id: {
                type: String,
                default: ''
            },
            data: {
                type: Object,
                default: null
            }
        },
        watch:{
            data:{
                handler(newValue) {
                    this.initOption(newValue);
                },
                deep:true
            }
        },
        mounted() {
            if(this.data!=null || this.id!=''){
                this.initOption(this.data);
            }
        },
        created() {},
        methods: {
            initOption( {
                            legendData=[],
                            xAxisData=[],
                            seriesData=[],
                            animation=true,
                        }={}){
                let myChartId = document.getElementById(this.id);
                //高度计算
//                this.chartssize(document.getElementById(chartPid),myChartId);
                let myChart = this.$echarts.init(myChartId);
                let option = {
                    tooltip: {
                            trigger: 'axis',
                            axisPointer: {
                                lineStyle: {
                                    color: {
                                        type: 'linear',
                                        x: 0,
                                        y: 0,
                                        x2: 0,
                                        y2: 1,
                                        colorStops: [{
                                            offset: 0,
                                            color: 'rgba(0, 255, 233,0)'
                                        }, {
                                            offset: 0.5,
                                            color: 'rgba(255, 255, 255,1)',
                                        }, {
                                            offset: 1,
                                            color: 'rgba(0, 255, 233,0)'
                                        }],
                                        global: false
                                    }
                                },
                            }
                        },
                    grid: {
                        top: '15%',
                        left: '5%',
                        right: '7%',
                        bottom: '8%',
                        containLabel: true
                    },
//                    legend: {
//                        show: true,
//                        itemWidth:5,
//                        itemHeight:20,
//                        data:this.data.legendData,
////                        data:['1','2','3'],
//                        textStyle: {
//                            color: '#B4B4B4'
//                        },
//                        top: '10%',
//                        left:'10%'
//                    },
                    xAxis: {
                        type: 'category',
                        boundaryGap: false,
                        data: xAxisData,
                        axisLabel: {
                            textStyle: {
                                color: '#fff'
                            },
                            formatter: function(params) {
                                return params.split(' ')[0] + '\n' + params.split(' ')[1]
                            }
                        }
                    },
                    yAxis: [{
                        type: 'value',
                        min: 0,
                        splitNumber: 4,
                        splitLine: {
                            show: true,
                            lineStyle: {
                                color: 'rgba(255,255,255,0.1)'
                            }
                        },
                        axisLine: {
                            show: true,
                            lineStyle: {
                                color: '#bcccc8'
                            },
                        },
                        axisLabel: {
                            show: true,
                            margin: 20,
                            textStyle: {
                                color: '#d1e6eb',

                            },
                        },
                        axisTick: {
                            show: true,
                        },
                    }],
                    dataZoom: [{
                        "show": true,
                        "height": 12,
                        "xAxisIndex": [
                            0
                        ],
                        bottom:'2%',
                        start: 0,
                        end: 100,
                        handleSize: '100%',
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
                    series:seriesData,
                    animation:animation,
                };
                myChart.clear();
                myChart.setOption(option,true);
                setTimeout(function() {
                    window.addEventListener('resize', ()=> {
                        myChart.resize();
                    })
                }, 200)
            },
            //为图表计算高度
            chartssize(container, charts) {
                function getStyle(el, name){
                    if (window.getComputedStyle) {
                        return window.getComputedStyle(el, null);
                    } else {
                        return el.currentStyle;
                    }
                }
                let wi = getStyle(container, 'width').width;
                let hi = getStyle(container, 'height').height;
                charts.style.height = hi;
            }
        }

    };
</script>

<style scoped>
    .echart_container{
        /*height:185px;*/
        width:100%;
        height:100%;
    }
</style>