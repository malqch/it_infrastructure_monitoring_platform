<template>
    <div class="business-container">
        <div class="chart" id="chart_bot1"></div>
    </div>
</template>

<script>
    const echarts = require("echarts/lib/echarts");
    require("echarts/lib/chart/pie");
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
                let myChart = echarts.init(document.getElementById('chart_bot1'));
                let color = ['#ff4343', '#f69846', '#f6d54a', '#45dbf7', '#f69846', '#44aff0', '#4777f5', '#5045f6', '#ad46f3', '#f845f1'];
                let names = ["居住", "生产", "经营", "办公", "仓储", "其他"];
                let data = [1114, 444, 501, 468, 478, 431]
                let list = []
                let total = 0
                for (let i in data) {
                    total += data[i]
                }

                let placeHolderStyle = {
                    normal: {
                        label: {
                            show: false
                        },
                        labelLine: {
                            show: false
                        },
                        color: 'rgba(0, 0, 0, 0)',
                        borderColor: 'rgba(0, 0, 0, 0)',
                        borderWidth: 0
                    }
                };

                let rich = {
                    white: {
                        align: 'center',
                        padding: [3, 0]
                    }
                };

                for (let i in data) {
                    list.push({
                        value: data[i],
                        name: names[i],
                        itemStyle: {
                            normal: {
                                borderWidth: 5,
                                shadowBlur: 20,
                                borderColor: color[i],
                                shadowColor: color[i],
                                color: color[i]
                            }
                        }
                    }, {
                        value: total / 30,
                        name: '',
                        itemStyle: placeHolderStyle
                    })
                }

                let func = (params) => {
                    let percent = ((params.value / total) * 100).toFixed(1)
                    let name = params.name.replace(/\n/g, '')
                    if (params.name !== '') {
                        return name + '\n{white|' + percent + '%}'
                    } else {
                        return ''
                    }
                }
                let option = {
//                    backgroundColor: '#04243E',
                    tooltip: {
                        show: false
                    },
                    legend: {
                        orient: 'vertical',
                        data: names,
                        icon: 'circle',
                        right: '5px',
                        top: '10px',
                        textStyle: {
                            color: '#fff',
                            fontSize: 20
                        }
                    },
                    series: [{
                        name: '',
                        type: 'pie',
                        clockWise: false,
                        startAngle: '90',
                        center: ['50%', '50%'],
                        radius: ['50%', '51%'],
                        hoverAnimation: false,
                        itemStyle: {
                            normal: {
                                label: {
                                    show: true,
                                    position: 'outside',
                                    formatter: func,
                                    rich: rich
                                },
                                labelLine: {
                                    length: 10,
                                    length2: 10,
                                    show: true,
                                    color: '#00ffff'
                                }
                            }
                        },
                        data: list,
                        animationType: 'scale',
                        animationEasing: 'elasticOut',
                        animationDelay: function(idx) {
                            return idx * 50;
                        }
                    },
                        {
                            name: '',
                            type: 'pie',
                            center: ['50%', '50%'],
                            radius: ['49%', '49%'],
                            itemStyle: {
                                color: 'transparant'
                            },
                            startAngle: '90',
                            data: [{
                                value: total,
                                name: '',
                                label: {
                                    normal: {
                                        show: true,
                                        formatter: '{c|{c}}',
                                        rich: {
                                            c: {
                                                color: 'rgb(98,137,169)',
                                                fontSize: 14,
                                                fontWeight: 'bold',
                                                lineHeight: 5
                                            }
                                        },
                                        textStyle: {
                                            fontSize: 28,
                                            fontWeight: 'bold'
                                        },
                                        position: 'center'
                                    }
                                }
                            }]
                        }
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