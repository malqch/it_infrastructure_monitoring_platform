<template>
    <div class="box-container">
        <div style="height:100%;width:100%">
            <div class="bodytable"  :id='id'>
                <ul :data="redisListData" v-for="(item,index) in this.data" :key="index">
                    <li>
                        <span>{{item.name}}:</span>
                        <span>{{item.value}}</span>
                    </li>
                </ul>
            </div>
        </div>
    </div>
</template>

<script>
    export default {
        name: "redisList",
        data(){
            return{
                redisListData:[],
                ChartLineGraph:null,
                num: 0,
                animate:false,

            }
        },
        //  深度监听 父组件刚开始没有值，只有图标的配置项
        //  父组件ajax请求后改变数据的值，传递过来，图标已生成，监听传过来的值的改变
        // deep:true.深度监听，确保data中子项修改也能监听到
        watch:{
            data:{
                handler(newValue) {
                    this.drawliquidFill(newValue);
                },
                deep:true
            }
        },
        props:{
            id: {
                type: String,
                default: ''
            },
            data: {
                type: Array,
                default:function () { return [] }
            },
            height: {
                type: Number,
                default: 40
            },
            lineNum: {
                type: Number,
                default: 5
            }
        },
        computed: {
            top(){
//                return -this.activeIndex * this.moveDistance + "px"; //定义移动的单元高度
                return -this.activeIndex * 35 + "px"; //定义移动的单元高度
            },
            transform: function () {
                return 'translateY(-' + this.num * this.height + 'px)'
            }

        },
        mounted() {
            this.drawliquidFill(this.data);
        },
        created(){
//            this.drawliquidFill(this.data);
//            setInterval(this.scroll(this.data),3000)
//            this.scroll(this.data)
        },
        methods:{
            // drawliquidFill(redisListData){
            //     let _this = this;
            //     /*setInterval(function () {
            //         if (_this.num !== dutyRateData.length) {
            //             _this.num++
            //         } else {
            //             _this.num = 0
            //         }
            //     }, 3000)*/
            //     /*this.animate=true;    // 因为在消息向上滚动的时候需要添加css3过渡动画，所以这里需要设置true
            // setTimeout(()=>{
            //         dutyRateData.push(dutyRateData[0]);
            //         dutyRateData.shift();
            //         this.animate=false;  // margin-top 为0 的时候取消过渡动画，实现无缝滚动
            //     },5000)*/

            //     /*window.addEventListener("resize",function () {
            //         _this.diskEcharts.resize();
            //     });*/
            // },
            /*scroll(dutyRateData){
                this.animate=true;    // 因为在消息向上滚动的时候需要添加css3过渡动画，所以这里需要设置true

                /!*setTimeout(()=>{
                    dutyRateData.push(dutyRateData[0]);  // 将数组的第一个元素添加到数组的
                    dutyRateData.shift();               //删除数组的第一个元素
                    this.animate=false;  // margin-top 为0 的时候取消过渡动画，实现无缝滚动
                },5000)*!/
            }*/
        },
        beforeDestroy() {
            clearInterval(this.ChartLineGraph);
            this.ChartLineGraph = null;
        }
    }

</script>

<style lang="scss" scoped>
	.box-container{
		padding-top: 10px;
	}
  ul{
      list-style: none;
      li{
          line-height: 30px;
          color:#b08ff9;
          font-size: 12px;

      }
  }
.bodytable{
    height: 235px;
	padding-left: 10px;
    overflow-y: scroll;
	
    scrollbar-width:none; /* Firefox */
    -ms-overflow-style: none; /* IE 10+ */
}
  ::-webkit-scrollbar {
      display: none; /* Chrome Safari */
  }


</style>