<template>
    <div>
        <div class="contain" :style="{height: this.height}">
            <el-row class="contain_margin_top row-bg" type="flex" justify="center">
                <el-col :span="6">
                    <img src="../../assets/img/index/user3.png">
                </el-col>
                <el-col :span="6" :offset="1">
                    <dl class="text_index">
                        <dt class="_wel">欢迎进入</dt>
                        <dd class="wel_sys">系统管理页面</dd>
                    </dl>
                </el-col>
            </el-row>
        </div>
    </div>
</template>
<script>
    export default{
        name:'sys',
        data(){
            return{
                height:0
            }
        },
        computed:{
        },
        created(){
            setTimeout(()=>{
                this.Cheight();
            },200)

        },
        methods:{
            Cheight(){
                this.height=(document.getElementsByClassName('content')[0].clientHeight-20)+'px';
            }
        }
    }
</script>
<style lang="scss" scoped>
    @import "../../assets/css/fonts/font.css";
    /*@import "../../assets/scss/echarts";*/
    .contain{
        background:#b7cff3;
    }
    .left_img{
        margin-left:16%;
    }
    ._wel{
        letter-spacing:5px;
        font-size: 36px;
    }
    .wel_sys{
        font-size:28px;
        margin-top: 8px;
    }
.text_index{
   letter-spacing: 4px;
    /*color: #4995ec;*/
    color:#fff;
    margin-top:110px;
}
.contain_margin_top{
    padding-top:10%;
}
.serve_select p{
    color:#03c2ec;
    font-size:12px;
    padding:0px 0 0 10px;
    font-weight: 600;
}
.grid-content {
    display: flex;
    align-items: center;
    height: 80px;
}

.grid-cont-right {
    flex: 1;
    text-align: center;
    font-size: 14px;
    color: #999;
}

.grid-num {
    font-size: 30px;
    font-weight: bold;
}

.grid-con-icon {
    font-size: 50px;
    width: 100px;
    height: 110px;
    text-align: center;
    line-height: 100px;
    color: rgb(45, 140, 240);
}

/*.grid-con-1 .grid-con-icon {*/
    /*background: rgb(45, 140, 240);*/
/*}*/

.grid-con-1 .grid-num {
    color: rgb(45, 140, 240);
}

.grid-con-2 .grid-con-icon {
    background: rgb(100, 213, 114);
}

.grid-con-2 .grid-num {
    color: rgb(45, 140, 240);
}

.grid-con-3 .grid-con-icon {
    background: rgb(242, 94, 67);
}

.grid-con-3 .grid-num {
    color: rgb(242, 94, 67);
}

.user-info {
    display: flex;
    align-items: center;
    padding-bottom: 20px;
    border-bottom: 2px solid #ccc;
    margin-bottom: 20px;
}

.user-avator {
    width: 120px;
    height: 120px;
    border-radius: 50%;
}

.user-info-cont {
    padding-left: 50px;
    flex: 1;
    font-size: 14px;
    color: #999;
}

.user-info-cont div:first-child {
    font-size: 30px;
    color: #222;
}

.user-info-list {
    font-size: 14px;
    color: #999;
    line-height: 25px;
}

.user-info-list span {
    margin-left: 70px;
}

.mgb20 {
    margin-bottom: 20px;
}

.todo-item {
    font-size: 14px;
}

.todo-item-del {
    text-decoration: line-through;
    color: #999;
}

.schart {
    width: 100%;
    height: 300px;
}
</style>
