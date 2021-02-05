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
				isCollapse(newValue){
					alert(newValue)        
					setTimeout(() => {
						let myChartId = document.getElementById(id);
						this.$echarts.init(myChartId).resize();
					},50);
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
            drawLineGraph(id,charts){
                let myChart = this.$echarts.init(document.getElementById(id));
				let myChartId = document.getElementById(id);
				myChartId.style.width=(window.innerWidth-250)/3+"px";
                this.optionBusiness= {
                        color: ['#ffdb5c','#ff9f7f','#fb7293','#e7bcf3','#8378ea','#37a2da','#32c5e9','#9fe6b8',],
                        tooltip : {
                            trigger: 'item',
                            formatter: "{b} <br/>数量: {c} <br/> 占比: {d}%"
                        },
                        toolbox: {
                            show : true,
                        },
                    // 旁边的备注
                        legend: {
                            type: 'scroll',
                            orient: 'vertical',
                            left: '2%',
                            top: 'top',
                            bottom: 20,
                            textStyle: {
                                color:'#8C8C8C'
                            }
                        },
                        series : [
                            {
                                name:'',
                                type:'pie',
                                radius : [0, 60], //调整饼图大小
                                center: ['50%', '58%'],
                                data: charts
                            }
                        ]

                };
                myChart.setOption(this.optionBusiness);
				this.$echarts.init(myChartId).resize();
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
        width: 100%;
        height: 220px;
    }
</style>