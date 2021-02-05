<template>
    <div :id=id ref="data" class="echart_container"></div>
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
                this.initOption(this.id,this.data);
            }
        },
        created() {},
        methods: {
            initOption({//options里需要用的数据这里作为参数从data里面取值
                           myColor=[],
                           yAxisData = [],
                           seriesData = []
                       } = {}){
                let myChart = this.$echarts.init(document.getElementById(this.id));
                /*const myColor = ['#eb2100', '#eb3600', '#d0570e', '#d0a00e', '#34da62', '#00e9db', '#00c0e9', '#0096f3', '#33CCFF', '#33FFCC'];*/
                myColor=this.data.myColor;
                let option = {
                    tooltip: {
                        trigger: 'axis'
                    },
                    grid: {
                        top: '5%',
                        left: '6%',
                        right: '8%',
                        bottom: '2%',
                        containLabel: true
                    },
                    xAxis: [{
                        show: false,
                    }],
                    yAxis: [{
                        axisTick: 'none',
                        axisLine: 'none',
                        offset: '10',
                        axisLabel: {
                            textStyle: {
                                color: '#ffffff',
                                fontSize: '12',
                            }
                        },
                        data: this.data.yAxisData
                    }, {
                        data: []
                    }, {
                        data: [],
                    }],
                    series: [{
                        type: 'bar',
                        yAxisIndex: 0,
                        data: this.data.seriesData,
                        label: {
                            normal: {
                                formatter:'{c}%',
                                show: true,
                                position: 'right',
                                textStyle: {
                                    color: '#ffffff',
                                    fontSize: '12',
                                }
                            }
                        },
                        barWidth: 10,
                        itemStyle: {
                            normal: {
                                color: function(params) {
                                    const num = myColor.length;
                                    return myColor[params.dataIndex % num]
                                },
                            }
                        },
                        z: 2
                    }, {
                        name: '白框',
                        type: 'bar',
                        yAxisIndex: 1,
                        barGap: '-100%',
                        data: [99, 99.5, 99.5],
                        barWidth: 13,
                        itemStyle: {
                            normal: {
                                color: '#24273e',
                                barBorderRadius: 5,
                            }
                        },
                        z: 1
                    }, {
                        name: '外框',
                        type: 'bar',
                        yAxisIndex: 2,
                        barGap: '-100%',
                        data: [100, 100, 100],
                        barWidth: 16,
                        itemStyle: {
                            normal: {
                                color: function(params) {
                                    const num = myColor.length;
                                    return myColor[params.dataIndex % num]
                                },
                                barBorderRadius: 5,
                            }
                        },
                        z: 0
                    },
                        {
                            name: '外圆',
                            type: 'scatter',
                            hoverAnimation: false,
                            data: [0, 0, 0],
                            yAxisIndex: 2,
                            symbolSize: 20,
                            itemStyle: {
                                normal: {
                                    color: function(params) {
                                        const num = myColor.length;
                                        return myColor[params.dataIndex % num]
                                    },
                                    opacity: 1,
                                }
                            },
                            z: 2
                        }
                    ]
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
    .echart_container{
        height:220px;
        /*padding:6px 0;*/
    }
</style>