<template>
    <div class="box-container">
        <div :id=id :data=charts  class="echart-container"></div>
    </div>
</template>

<script>
    export default {
        name: "baseEchartsAllComponent",
        data(){
            return{
                charts:null,
                ChartLineGraph:null,
            }
        },
        watch:{
            data:{
                handler(newValue) {
                    this.drawLineGraph(this.id,newValue);
                },
                deep:true
            }

        },
        //接收父组件传过来的参数
        props:{
            id: {
                type: String,
                default: ''
            },
            data: {
                type: Array,
                default: null
            }
        },
        mounted() {
            if (this.data != null) {
                this.drawLineGraph(this.id, this.data);
            }
        },
        methods:{
            drawLineGraph(id, charts){
                let myChart = document.getElementById(id);
                this.ChartLineGraph = this.$echarts.init(myChart);
                this.optionBusiness= {
                    color: ['#ffdb5c','#ff9f7f','#fb7293','#e7bcf3','#8378ea','#37a2da','#32c5e9','#9fe6b8',],
                    tooltip : {
                        trigger: 'item',
                        formatter: "{b} <br/>数量: {c} <br/>占比: {d}%"
                    },
                    toolbox: {
                        show : true,

                    },
                    // 旁边的备注
                    legend: {
                        type:"scroll",
                        orient: 'vertical',
                        right:'6%',
                        align:'left',
                        top:'top',
                        textStyle: {
                            color:'#8C8C8C'
                        },
                        height:150
                    },
                    series : [
                        {
                            name:'业务',
                            type:'pie',
                            radius : [0, 70], //调整饼图大小
                            data: charts
                        }
                    ]

                };
                this.ChartLineGraph.setOption(this.optionBusiness);

            },
            // 格式化数据
            /*getData(charts) {
                let seriesDataObj = {} //每条数据
                let seriesData = []
                charts.map((item) => {
                    seriesDataObj = {
                        name: item.operate_system,
                        value: item.operate_system__count,
                    }
                    seriesData.push(seriesDataObj)
                })
                console.log(seriesData,111)
                return seriesData
            },*/
        },
        beforeDestroy() {
            clearInterval(this.ChartLineGraph);
            this.ChartLineGraph = null;
        }
    }

</script>

<style lang="scss" scoped>
    .echart-container {
        width: 573px;
        height: 220px;
    }
</style>
