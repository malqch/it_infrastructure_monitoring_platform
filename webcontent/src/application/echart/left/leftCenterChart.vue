<template>
    <div class="business-container">
        <div class="chart" id="chart_center1"></div>
    </div>
</template>

<script>
    const echarts = require("echarts/lib/echarts");
    require("echarts/lib/chart/line");
    export default {
        name: "business",
        data() {
            return {

            }
        },
        mounted() {
            this.getEchartLeft1();
        },
        methods: {
            getEchartLeft1() {
                // 实例化对象
                let myChart = echarts.init(document.getElementById('chart_center1'));
                // 指定配置和数据
                let option = {
                    // backgroundColor: '#080b30',
                    title: {
                        text: '哎呦,不错哦',
                        textStyle: {
                            align: 'center',
                            color: '#fff',
                            fontSize: 20,
                        },
                        top: '5%',
                        left: 'center',
                    },
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
                        },
                    },
                    grid: {
                        top: '15%',
                        left: '5%',
                        right: '5%',
                        bottom: '15%',
                        // containLabel: true
                    },
                    xAxis: [{
                        type: 'category',
                        axisLine: {
                            show: true
                        },
                        splitArea: {
                            // show: true,
                            color: '#f00',
                            lineStyle: {
                                color: '#f00'
                            },
                        },
                        axisLabel: {
                            color: '#fff'
                        },
                        splitLine: {
                            show: false
                        },
                        boundaryGap: false,
                        data: ['A', 'B', 'C', 'D', 'E', 'F'],

                    }],

                    yAxis: [{
                        type: 'value',
                        min: 0,
                        // max: 140,
                        splitNumber: 4,
                        splitLine: {
                            show: true,
                            lineStyle: {
                                color: 'rgba(255,255,255,0.1)'
                            }
                        },
                        axisLine: {
                            show: false,
                        },
                        axisLabel: {
                            show: false,
                            margin: 20,
                            textStyle: {
                                color: '#d1e6eb',

                            },
                        },
                        axisTick: {
                            show: false,
                        },
                    }],
                    series: [{
                        name: '注册总量',
                        type: 'line',
                        // smooth: true, //是否平滑
                        showAllSymbol: true,
                        // symbol: 'image://./static/images/guang-circle.png',
                        symbol: 'circle',
                        symbolSize: 25,
                        lineStyle: {
                            normal: {
                                color: "#6c50f3",
                                shadowColor: 'rgba(0, 0, 0, .3)',
                                shadowBlur: 0,
                                shadowOffsetY: 5,
                                shadowOffsetX: 5,
                            },
                        },
                        label: {
                            show: true,
                            position: 'top',
                            textStyle: {
                                color: '#6c50f3',
                            }
                        },
                        itemStyle: {
                            color: "#6c50f3",
                            borderColor: "#fff",
                            borderWidth: 3,
                            shadowColor: 'rgba(0, 0, 0, .3)',
                            shadowBlur: 0,
                            shadowOffsetY: 2,
                            shadowOffsetX: 2,
                        },
                        tooltip: {
                            show: false
                        },
                        areaStyle: {
                            normal: {
                                color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [{
                                    offset: 0,
                                    color: 'rgba(108,80,243,0.3)'
                                },
                                    {
                                        offset: 1,
                                        color: 'rgba(108,80,243,0)'
                                    }
                                ], false),
                                shadowColor: 'rgba(108,80,243, 0.9)',
                                shadowBlur: 20
                            }
                        },
                        data: [502.84, 205.97, 332.79, 281.55, 398.35, 214.02, ]
                    },
                        {
                            name: '注册总量',
                            type: 'line',
                            // smooth: true, //是否平滑
                            showAllSymbol: true,
                            // symbol: 'image://./static/images/guang-circle.png',
                            symbol: 'circle',
                            symbolSize: 25,
                            lineStyle: {
                                normal: {
                                    color: "#00ca95",
                                    shadowColor: 'rgba(0, 0, 0, .3)',
                                    shadowBlur: 0,
                                    shadowOffsetY: 5,
                                    shadowOffsetX: 5,
                                },
                            },
                            label: {
                                show: true,
                                position: 'top',
                                textStyle: {
                                    color: '#00ca95',
                                }
                            },

                            itemStyle: {
                                color: "#00ca95",
                                borderColor: "#fff",
                                borderWidth: 3,
                                shadowColor: 'rgba(0, 0, 0, .3)',
                                shadowBlur: 0,
                                shadowOffsetY: 2,
                                shadowOffsetX: 2,
                            },
                            tooltip: {
                                show: false
                            },
                            areaStyle: {
                                normal: {
                                    color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [{
                                        offset: 0,
                                        color: 'rgba(0,202,149,0.3)'
                                    },
                                        {
                                            offset: 1,
                                            color: 'rgba(0,202,149,0)'
                                        }
                                    ], false),
                                    shadowColor: 'rgba(0,202,149, 0.9)',
                                    shadowBlur: 20
                                }
                            },
                            data: [281.55, 398.35, 214.02, 179.55, 289.57, 356.14, ],
                        },
                    ]
                };

                // 把配置给实例对象
                myChart.setOption(option, true);
                window.addEventListener('resize', () => {
                    myChart.resize();
                });
            },
        },
        beforeDestroy() {

        }
    };
</script>

<style lang="scss" scoped>
    .business-container {
        .chart {
            height: 3.2rem;
        }
    }
</style>