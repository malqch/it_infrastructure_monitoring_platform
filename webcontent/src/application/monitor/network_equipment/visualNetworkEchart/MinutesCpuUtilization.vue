<template>
    <div :id=id  ref="data"  class="echart_container"></div>
</template>

<script>
    export default{
        name:'utilizationCharts',
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
            initOption({
                           title='',
                           legendData=[],
                           xAxisData=[],
                           seriesData=[],
                           animation=true
                       }){
                let myChart = this.$echarts.init(document.getElementById(this.id));
                let option = {
                    title: {
                        text: title,
                        left: "5%",
                        top:'3%',
                        bottom:'5%',
                        textStyle: {
                            fontFamily: "monospace",
                            color: '#0dd1ec',
                            fontSize: '14'
                        }
                    },
                    tooltip: {
                        trigger: 'axis'
                    },
                    legend: {
                        show: true,
                        itemHeight: 5,
                        itemWidth: 24,
                        data:legendData,
                        textStyle: {
                            color: '#B4B4B4'
                        },
                        top: '0%',
                        left:'30%'
                    },
                    grid: {
                        top: '19%',
                        left: '4%',
                        right: '10%',
                        bottom: '10%',
                        containLabel: true
                    },
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
                    yAxis: {
//                        name: charts.unit,
                        type: 'value',
                        axisLabel: {
                            formatter: '{value}',
                            textStyle: {
                                color: '#fff'
                            }
                        },
                        splitLine: {
                            lineStyle: {
                                type: "dashed",
                                color: '#5a637f',
                            }
                        },
                        axisLine: {
                            lineStyle: {
                                color: '#5a637f'
                            }
                        },
                        axisTick:{
                            show:false
                        },
                        minorTick:{
                            show:false
                        }
                    },
                    dataZoom: [{
                        "show": true,
                        "height": 12,
                        "xAxisIndex": [
                            0
                        ],
                        bottom:'2%',
                        start: 80,
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
                    animation:animation

                };
                myChart.setOption(option,true);
                setTimeout(function() {
                    window.addEventListener('resize', ()=> {
                        myChart.resize();
                    })
                }, 200)
            }
        }

    };
</script>

<style scoped>
    /*.echart_container{
        width:100%;
        height:100%;
    }*/
</style>