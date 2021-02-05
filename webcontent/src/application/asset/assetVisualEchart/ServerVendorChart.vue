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
                charts: null,
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
            // 格式化数据
            drawLineGraph(id, charts){
                let titleArr = [],
                    seriesArr = [];
                charts.forEach(function(item, index) {
                    titleArr.push({
                        text: item.name,
                        left: index * 15 + 4 + '%',
                        top: '8%',
                        textAlign: 'top',
                        textStyle: {
                            fontWeight: '600',
                            fontSize: '12',
                            color: '#03c2ec',
                            textAlign: 'top',
                        },
                    });
                    seriesArr.push({
                        name: item.name,
                        type: 'pie',
                        center: [index * 15 + 7 +'%','63%'],
                        radius: [0, 50],
                        data: item.value
                    })
                });
                let myChart = this.$echarts.init(document.getElementById(id));
				let myChartId = document.getElementById(id);
				myChartId.style.width=window.innerWidth-250+"px";
                this.optionBusiness = {
                    color: ['#ffdb5c','#ff9f7f','#fb7293','#e7bcf3','#8378ea','#37a2da','#32c5e9','#9fe6b8',],
                    tooltip : {
                        trigger: 'item',
                        formatter: "{b} <br/>数量: {c} <br/>占比: {d}%"
                    },
                    toolbox: {
                        show : true
                    },
                    // 旁边的备注
                    legend: {
                        type:"scroll",
                        orient: 'vertical',
                        right:'0%',
                        align:'left',
                        top:'10%',
                        textStyle: {
                            color:'#8C8C8C'
                        },
                        height:150
                    },
                    title: titleArr,
                    series: seriesArr,

                };
                myChart.setOption(this.optionBusiness);
				//this.$echarts.init(myChartId).resize();
                setTimeout(function() {
                    window.addEventListener('resize', ()=> {
                        myChart.resize();
                    })
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
        height: 240px;
    }
</style>
