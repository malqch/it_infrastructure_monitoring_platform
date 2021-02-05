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
                           xAxisData = [],
                           seriesData = []
                       } = {}){
                let myChart = this.$echarts.init(document.getElementById(this.id));
                let option = {
                    tooltip: {
                        trigger: 'axis'
                    },
                    grid: {
                        top: '15%',
                        left: '4%',
                        right: '5%',
                        bottom: '8%',
                        containLabel: true
                    },
                    xAxis: [{
                        type: 'category',
                        data: xAxisData,
                        axisLine: {
                            lineStyle: {
                                color: 'rgba(255,255,255,0.12)'
                            }
                        },
                        axisLabel: {
                            margin: 10,
                            color: '#e2e9ff',
                            textStyle: {
                                fontSize: 14
                            },
                        },
                    }],
                    yAxis: [{
                        axisLabel: {
                            formatter: '{value}',
                            color: '#e2e9ff',
                        },
                        axisLine: {
                            show: false,
                            lineStyle: {
                                color: 'rgba(255,255,255,1)'
                            }
                        },
                        splitLine: {
                            lineStyle: {
                                color: 'rgba(255,255,255,0.12)'
                            }
                        }
                    }],
                    series:seriesData
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
        height:185px;
        /*padding:6px 0;*/
    }
</style>